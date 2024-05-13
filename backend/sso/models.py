from django.contrib.sessions.models import Session
import base64, json, logging, pyotp, datetime, secrets, time

from email.mime.text import MIMEText

from django.contrib.sessions.backends.db import SessionStore as DBStore
from django.contrib.sessions.base_session import AbstractBaseSession
from django.contrib.sessions.management.commands import clearsessions

from django.db import models, transaction
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import constant_time_compare
from django.template.loader import render_to_string

from rest_framework.exceptions import Throttled, ParseError

from core.utils import housekeeping_signal
from .utils import GMailAPI
from .  import TOTP_SESSION_KEY

logger = logging.getLogger(__name__)

def generate_mail_otp():
    return base64.b64encode(secrets.token_bytes(3)).decode('utf-8')

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
        message = MIMEText(render_to_string(
            self.template,
            {'otp' : self.otp, 'reason' : reason}),
            "html"
        )
        message["To"] = self.email
        message["From"] = f"KISA Web Team <{GMailAPI.FROM_MAIL}>"
        message["Subject"] = "[No Reply] Your Personal Authentication for KISA Services"

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        if GMailAPI.client and GMailAPI.client.service:
            GMailAPI.client.service.users().messages().send(userId="me", body=create_message).execute()
        else:
            logger.warning(f"Mail OTP code send failure to {self.email}")

    @classmethod
    def clear_expired(cls):
        now = datetime.datetime.now()
        for session in cls.objects.all():
            if now - session.time_started > cls.MAX_LIFETIME:
                session.delete()


class TOTPDevice(models.Model):
    VALID_WINDOW = 2
    ON_DELAY_INIT = 0.25

    secret = models.CharField(default=pyotp.random_base32)
    last_failed_attempt_time = models.DateTimeField(default=datetime.datetime.now)
    next_delay_sec = models.FloatField(default=ON_DELAY_INIT)
    on_cooldown = models.BooleanField(default=False)

    def verify(self, token):
        result = pyotp.TOTP(self.secret).verify(token, valid_window=self.VALID_WINDOW)
        with transaction.atomic():
            device = TOTPDevice.objects.select_for_update().get(pk=self.pk)
            wait_time = (device.last_failed_attempt_time - datetime.datetime.now()) + device.next_delay_sec*datetime.timedelta(seconds=1)
            if device.on_cooldown and wait_time > datetime.timedelta(seconds=0):
                raise Throttled(wait=wait_time.total_seconds())
            result = result and not TOTPUsedToken.check_used(token, self)
            if result:
                device.on_cooldown = False
                device.next_delay_sec = device.ON_DELAY_INIT
                TOTPUsedToken.insert(token, device)
            else:
                device.on_cooldown = True
                device.next_delay_sec *= 2
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


class User(AbstractUser):
    # make all fields except KAIST UID 'blank=true' because some fields might be empty
    # these are all the fields KISA registered for
    KSSO_KEYS_AND_FIELDS = [
        ('kaist_uid', 'kaist_uid'),
        ('ku_kname', 'korean_name'),
        ('displayname', 'full_name'),
        ('sn', 'first_name'),
        ('givenname', 'last_name'),
        ('ku_born_date', 'dob'),
        ('c', 'nationality'),
        ('ku_sex', 'sex'),
        ('mail', 'kaist_email'),
        ('ku_ch_mail', 'external_email'),
        ('ku_employee_number', 'employee_number'),
        ('ku_std_no', 'student_number'),
        ('ku_acad_org', 'bachelors_department_code'),
        ('ku_acad_name', 'bachelors_department_name'),
        ('ku_campus', 'campus'),
        ('title', 'title_english'),
        ('ku_psft_user_status', 'student_status_english'),
        ('ku_psft_user_status_kor', 'student_status_korean'),
        ('ku_acad_prog_code', 'degree_code'),
        ('ku_acad_prog', 'degree_name_korean'),
        ('ku_acad_prog_eng', 'degree_name_english'),
        ('employeeType', 'employee_type'),
        ('ku_prog_effdt', 'student_admission_datetime'),
        ('ku_stdnt_type_id', 'student_type_id'),
        ('ku_stdnt_type_class', 'student_type_class'),
        ('ku_category_id', 'student_category_id'),
        ('ku_prog_start_date', 'student_enrollment_date'),
        ('ku_prog_end_date', 'student_graduation_date'),
        ('acad_ebs_org_id', 'student_department_id'),
        ('uid', 'sso_id'),
        ('acad_ebs_org_name_eng', 'student_department_name_english'),
        ('acad_ebs_org_name_kor', 'student_department_name_korean'),
    ]

    # kaist_uid is not student number (find below for another field named student_number)
    kaist_uid = models.IntegerField(default = 0)  # kaist_uid

    korean_name = models.CharField(max_length=100, blank=True, null=True)  # ku_kname
    full_name = models.CharField(max_length=100)  # displayname
    first_name = models.CharField(max_length=100)  # sn
    last_name = models.CharField(max_length=100)  # givenname

    dob = models.DateField(blank=True, null=True)  # ku_born_date
    nationality = models.CharField(max_length=100)  # c
    sex = models.CharField(max_length=20, blank=True, null=True)  # ku_sex

    kaist_email = models.EmailField(max_length=100, blank=True, null=True)  # mail
    external_email = models.EmailField(max_length=100, blank=True, null=True)  # ku_ch_mail

    employee_number = models.IntegerField(blank=True, null=True)  # ku_employee_number
    student_number = models.IntegerField(blank=True, null=True)  # ku_std_no
    bachelors_department_code = models.IntegerField(blank=True, null=True)  # ku_acad_org
    bachelors_department_name = models.CharField(max_length=200, blank=True, null=True)  # ku_acad_name
    campus = models.CharField(max_length=5, blank=True, null=True)  # ku_campus

    title_english = models.CharField(max_length=100)  # title
    student_status_english = models.CharField(max_length=100, blank=True, null=True)  # ku_psft_user_status
    student_status_korean = models.CharField(max_length=100, blank=True, null=True)  # ku_psft_user_status_kor

    degree_code = models.IntegerField(blank=True, null=True)  # ku_acad_prog_code
    degree_name_korean = models.CharField(max_length=100, blank=True, null=True)  # ku_acad_prog
    degree_name_english = models.CharField(max_length=100, blank=True, null=True)  # ku_acad_prog_eng

    employee_type = models.CharField(max_length=10)  # employeeType
    student_admission_datetime = models.DateTimeField(blank=True, null=True)  # ku_prog_effdt
    student_type_id = models.IntegerField(blank=True, null=True)  # ku_stdnt_type_id
    student_type_class = models.CharField(max_length=20, blank=True, null=True)  # ku_stdnt_type_class
    student_category_id = models.CharField(max_length=20, blank=True, null=True)  # ku_category_id

    student_enrollment_date = models.DateField(blank=True, null=True)  # ku_prog_start_date
    student_graduation_date = models.DateField(blank=True, null=True)  # ku_prog_end_date

    student_department_id = models.IntegerField(blank=True, null=True)  # acad_ebs_org_id
    sso_id = models.CharField(max_length=100, blank=True, null=True)  # uid
    student_department_name_english = models.CharField(max_length=100, blank=True, null=True)  # acad_ebs_org_name_eng
    student_department_name_korean = models.CharField(max_length=100, blank=True, null=True)  # acad_ebs_org_name_kor

    kisa_division = models.PositiveIntegerField(default=0)
    totp_device = models.ForeignKey(TOTPDevice, on_delete=models.CASCADE, blank=True, null=True)

    def is_valid_kaist_account(self):
        return self.kaist_uid != 0

    @classmethod
    def from_info_json(cls, user_info: dict):
        query = cls.objects.filter(kaist_uid=user_info['kaist_uid'])
        if query.exists():
            return query[0].update_from_info_json(user_info)
        user = cls()
        for key, field in cls.KSSO_KEYS_AND_FIELDS:
            if key in user_info:
                setattr(user, field, user_info[key])
        user.username = str(user.kaist_uid)
        user.set_unusable_password()

        # set the default mail to be the user's external mail or kaist mail
        # the external mail is first priority just in case KAIST SSO got hacked
        if user.external_email is not None and user.external_email != "":
            user.email = user.external_email
        elif user.kaist_email is not None and user.kaist_email != "":
            user.email = user.kaist_email

        user.full_clean()
        user.save()
        return user

    def get_info_json(self):
        info_json = dict()
        for key, field in self.KSSO_KEYS_AND_FIELDS:
            info_json[key] = getattr(self, field)
            if isinstance(info_json[key], datetime.date):
                info_json[key] = str(info_json[key])
        return info_json

    def update_from_info_json(self, user_info:dict):
        for key, field in self.KSSO_KEYS_AND_FIELDS:
            if key in user_info:
                setattr(self, field, user_info[key])
        self.full_clean()
        self.save()
        return self

    def is_kisa(self):
        return self.kisa_division != 0

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

# @receiver(signal=housekeeping_signal)
# def housekeeping_sig_listener(sender, **kwargs):
#     MailOTPSession.clear_expired()
#     TOTPUsedToken.clear_expired()
#     clearsessions.Command().handle()
