import logging, pyotp, datetime, secrets, math

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sessions.backends.db import SessionStore as DBStore
from django.contrib.sessions.management.commands import clearsessions

from django.db import models, transaction
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.crypto import constant_time_compare
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from rest_framework.exceptions import Throttled, ParseError

from core.utils import housekeeping_signal
from .  import TOTP_SESSION_KEY

logger = logging.getLogger(__name__)

def generate_mail_otp():
    return str(secrets.randbelow(1000000)).ljust(6, '0')

class MailOTPSession(models.Model):
    template = 'sso/email.html'
    MAX_ATTEMPT = 5
    MAX_LIFETIME = datetime.timedelta(minutes=8)
    data = models.JSONField(default=dict)
    otp = models.CharField(default=generate_mail_otp)
    time_started = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    available_attempts = models.SmallIntegerField(default=MAX_ATTEMPT)

    def verify(self, otp):
        result = constant_time_compare(self.otp, otp)
        with transaction.atomic():
            otp_obj = MailOTPSession.objects.select_for_update(nowait=True).filter(pk=self.pk).first()
            if otp_obj is None:
                raise ParseError()
            result = result and datetime.datetime.now() - self.time_started <= self.MAX_LIFETIME
            if result:
                data = otp_obj.data
                otp_obj.delete()
                return (data, 0)
            otp_obj.available_attempts -= 1
            available_attempts = otp_obj.available_attempts
            if otp_obj.available_attempts <= 0:
                otp_obj.delete()
            else:
                otp_obj.save()
            return (None, available_attempts)

    def send(self, reason:str):
        message = render_to_string(
            self.template,
            {'otp' : self.otp, 'reason' : reason}
        )
        to_mail = self.email
        from_email = f"KISA Web Team <{settings.DEFAULT_FROM_EMAIL}>"
        subject = "[No Reply] Your Personal Authentication for KISA Services"
        send_mail(subject, strip_tags(message), from_email, [to_mail])
        
    @classmethod
    def clear_expired(cls):
        now = datetime.datetime.now()
        for session in cls.objects.all():
            if now - session.time_started > cls.MAX_LIFETIME:
                session.delete()


class TOTPDevice(models.Model):
    VALID_WINDOW = 2
    DELAY_INIT = 0.25
    BRUTE_FORCE_TOLERANCE = 5
    MAX_DELAY = datetime.timedelta(days=1).seconds
    MAX_FAILED_ATTEMPTS = 200

    secret = models.CharField(default=pyotp.random_base32)
    last_failed_attempt_time = models.DateTimeField(default=datetime.datetime.now)
    num_failed_attempts = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)

    def verify(self, token):
        if not self.is_active:
            return False
        
        with transaction.atomic():
            device = TOTPDevice.objects.select_for_update(nowait=True).get(pk=self.pk)
            if device.num_failed_attempts > self.BRUTE_FORCE_TOLERANCE:
                wait_time = datetime.timedelta(seconds=self.DELAY_INIT*math.exp(device.num_failed_attempts-self.BRUTE_FORCE_TOLERANCE)) + datetime.datetime.now() - device.last_failed_attempt_time
                if wait_time > datetime.timedelta(seconds=0):
                    raise Throttled(wait=wait_time.total_seconds())
                
            result = pyotp.TOTP(self.secret).verify(token, valid_window=self.VALID_WINDOW) and not TOTPUsedToken.check_used(token, self)
            if result:
                device.num_failed_attempts = 0
                TOTPUsedToken.insert(token, device)
            else:
                device.num_failed_attempts = min(device.num_failed_attempts+1, self.MAX_FAILED_ATTEMPTS)
                device.last_failed_attempt_time = datetime.datetime.now()
            device.save()
            return result



class TOTPUsedToken(models.Model):
    time_used = models.DateTimeField()
    device = models.ForeignKey(TOTPDevice, on_delete=models.CASCADE)
    token = models.IntegerField()
    class Meta:
        index_together = ['device', 'token']

    @classmethod
    def check_used(cls, token, device):
        with transaction.atomic():
            result = cls.objects.select_for_update().filter(device=device, token=token).first()
            return result is not None and datetime.datetime.now() <= result.time_used + TOTPDevice.VALID_WINDOW * datetime.timedelta(seconds=30)

    @classmethod
    def insert(cls, token, device):
        with transaction.atomic():
            used_token = cls.objects.select_for_update().filter(device=device, token=token).first()
            if used_token is None:
                TOTPUsedToken(time_used=datetime.datetime.now(), device=device, token=token).save()

            else:
                used_token.time_used = datetime.datetime.now()

    @classmethod
    def clear_expired(cls):
        now = datetime.datetime.now()
        valid_duration = TOTPDevice.VALID_WINDOW * datetime.timedelta(seconds=30)
        for token in cls.objects.all():
            if now - token.time_used > valid_duration:
                token.delete()

class KISADivision(models.IntegerChoices):
        NONE = 0, _("None")
        WEB = 1, _("Web Division")
        FINANCE = 2, _("Finace Division")
        PPR = 3, _("PPR Division")
        EVENTS = 4, _("Events Division")
        WELFARE = 5, _("Welfare Division")
        SECRETARY = 6, _("Secretary")
        VICE_PRESIDENT = 7, _("Vice President")
        PRESIDENT = 8, _("President")

class User(AbstractUser):
    # make all fields except KAIST UID 'blank=true' because some fields might be empty
    # these are all the fields KISA registered for
    KSSO_KEYS_AND_FIELDS = [
        ('kaist_uid', 'kaist_uid'),
        ('user_id', 'sso_id'),

        ('user_eng_nm', 'english_name'), # english name
        ('user_nm', 'full_name'), # full name
        ('email', 'email'), # kaist mail
        ('busn_phone', 'business_phone'), # business phone number
        ('socps_cd', 'employeeType'), # employee type
        ('kaist_org_id', 'organization_id'), # kaist organization id
        ('campus_div_cd', 'campus'), # campus

        ('std_dept_kor_nm', 'student_department_name_korean'),
        ('std_dept_eng_nm', 'student_department_name_english'),
        ('std_status_kor', 'student_status_korean'),
        ('std_dept_id', 'student_department_id'),
        ('std_no', 'student_number'),

        ('emp_dept_kor_nm', 'employee_department_name_korean'),
        ('emp_dept_eng_nm', 'employee_department_name_english'),
        ('emp_status_kor', 'employee_status_korean'),
        ('emp_dept_id', 'employee_department_id'),
        ('emp_no', 'employee_number'),
    ]

    # kaist_uid is not student number (find below for another field named student_number)
    kaist_uid = models.IntegerField()  # kaist_uid
    sso_id = models.CharField(max_length=500) # user_id

    english_name = models.CharField(max_length=500)  # user_eng_nm
    full_name = models.CharField(max_length=500) # user_nm
    business_phone = models.CharField(max_length=500, blank=True, null=True) # busn_phone
    employee_type = models.CharField(max_length=10)  # socps_cd
    organization_id = models.IntegerField() # kaist_org_id
    campus = models.CharField(max_length=5) #  campus_div_cd

    student_department_name_korean = models.CharField(max_length=200, blank=True, null=True) # std_dept_kor_nm
    student_department_name_english = models.CharField(max_length=200, blank=True, null=True) # std_dept_eng_nm
    student_status_kor = models.CharField(max_length=100, blank=True, null=True) # std_status_kor
    student_department_id = models.IntegerField(blank=True, null=True) # std_dept_id
    student_number = models.IntegerField(blank=True, null=True) # std_no

    employee_department_name_korean = models.CharField(max_length=200, blank=True, null=True) # emp_dept_kor_nm
    employee_department_name_english = models.CharField(max_length=200, blank=True, null=True) # emp_dept_eng_nm
    employee_status_kor = models.CharField(max_length=100, blank=True, null=True) # emp_status_kor
    employee_department_id = models.IntegerField(blank=True, null=True) # emp_dept_id
    employee_number = models.IntegerField(blank=True, null=True) # emp_no

    kisa_division = models.IntegerField(choices=KISADivision.choices, default=KISADivision.NONE)
    totp_device = models.OneToOneField(TOTPDevice, on_delete=models.CASCADE)

    @classmethod
    def from_info_json(cls, user_info: dict):
        query = cls.objects.filter(kaist_uid=user_info['kaist_uid'])
        with transaction.atomic():
            if query.exists():
                user = query[0]
            else:
                user = cls()
                user.username = user_info['user_id'] + str(timezone.now()) # we don't have guarantee that 'user_id' will be unique
                user.set_unusable_password()
                user.totp_device = TOTPDevice()
                user.totp_device.save()
            
            for key, field in cls.KSSO_KEYS_AND_FIELDS:
                if key in user_info:
                    setattr(user, field, user_info[key])

            user.full_clean()
            user.save()
        return user
    
    def is_valid_kaist_account(self):
        return self.kaist_uid != 0
    
    def get_full_name(self):
        return self.full_name
    
    def get_short_name(self):
        return self.full_name

    def get_info_json(self):
        info_json = dict()
        for key, field in self.KSSO_KEYS_AND_FIELDS:
            info_json[key] = getattr(self, field)
            if isinstance(info_json[key], datetime.date):
                info_json[key] = str(info_json[key])
        return info_json

    def is_kisa(self):
        return self.kisa_division != KISADivision.NONE

    def is_verified(self, request):
        return TOTP_SESSION_KEY in request.session and bool(request.session[TOTP_SESSION_KEY])

    def __str__(self):
        return f'{self.get_full_name()}({self.email}, {self.kaist_uid})'

    @staticmethod
    def create(
        kaist_uid : int,
        email : str,
        first_name : str,
        last_name : str
    ):
        return User(
            kaist_uid = kaist_uid,
            email = email,
            first_name = first_name,
            last_name = last_name
        )

@receiver(signal=housekeeping_signal)
def housekeeping_sig_listener(sender, **kwargs):
    MailOTPSession.clear_expired()
    TOTPUsedToken.clear_expired()
    clearsessions.Command().handle()
