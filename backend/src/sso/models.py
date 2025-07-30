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
        ('socps_cd', 'employee_type'), # employee type
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

    REQUIRED_FIELDS = ['kaist_uid', 'sso_id', 'english_name', 'full_name', 'business_phone', 'employee_type', 'organization_id', 'campus']

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

    # def is_verified(self, request):
    #     return TOTP_SESSION_KEY in request.session and bool(request.session[TOTP_SESSION_KEY])

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
