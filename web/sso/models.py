import secrets

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import transaction

from tinymce.models import HTMLField

# Create your models here.


class User(AbstractUser):
    # make all fields except KAIST UID 'blank=true' because some fields might be empty
    # these are all the fields KISA registered for

    # kaist_uid is not student number (find below for another field named student_number)
    kaist_uid = models.IntegerField(primary_key=True)  # kaist_uid

    korean_name = models.CharField(max_length=100, blank=True, null=True)  # ku_kname
    full_name = models.CharField(max_length=100, blank=True, null=True)  # displayname
    first_name = models.CharField(max_length=100, blank=True, null=True)  # sn
    last_name = models.CharField(max_length=100, blank=True, null=True)  # givenname

    dob = models.DateField(blank=True, null=True)  # ku_born_date
    nationality = models.CharField(max_length=100, blank=True, null=True)  # c
    sex = models.CharField(max_length=20, blank=True, null=True)  # ku_sex

    kaist_email = models.EmailField(max_length=100, blank=True, null=True)  # mail
    external_email = models.EmailField(max_length=100, blank=True, null=True)  # ku_ch_mail

    employee_number = models.IntegerField(blank=True, null=True)  # ku_employee_number
    student_number = models.IntegerField(blank=True, null=True)  # ku_std_no
    bachelors_department_code = models.IntegerField(blank=True, null=True)  # ku_acad_org
    bachelors_department_name = models.CharField(max_length=200, blank=True, null=True)  # ku_acad_name
    campus = models.CharField(max_length=5, blank=True, null=True)  # ku_campus

    title_english = models.CharField(max_length=100, blank=True, null=True)  # title
    student_status_english = models.CharField(max_length=100, blank=True, null=True)  # ku_psft_user_status
    student_status_korean = models.CharField(max_length=100, blank=True, null=True)  # ku_psft_user_status_kor

    degree_code = models.IntegerField(blank=True, null=True)  # ku_acad_prog_code
    degree_name_korean = models.CharField(max_length=100, blank=True, null=True)  # ku_acad_prog
    degree_name_english = models.CharField(max_length=100, blank=True, null=True)  # ku_acad_prog_eng

    user_group = models.CharField(max_length=10, blank=True, null=True)  # employeeType
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
        ('employeeType', 'user_group'), 
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

    @classmethod
    def from_info_json(cls, user_info: dict):
        query = cls.objects.filter(kaist_uid=user_info['kaist_uid'])
        with transaction.atomic():
            if query.exists():
                return query[0].update_from_info_json(user_info)
            user = cls()
            for key, field in cls.KSSO_KEYS_AND_FIELDS:
                if key in user_info:
                    setattr(user, field, user_info[key])
            user.username = user_info.get('full_name', user.get_full_name()) # sometimes the displayname is not there
            for c in "!#$%^&*(),./<>?\\|":
                user.username = user.username.replace(c, '')
            user.username = user.username.strip()
            user.username = user.username.replace(' ', '_') + '_' + secrets.token_hex(4)
            user.set_unusable_password()
            user.full_clean()
            user.save()
        return user
        
    def update_from_info_json(self, user_info: dict):
        for key, field in self.KSSO_KEYS_AND_FIELDS:
            if key in user_info:
                setattr(self, field, user_info[key])
        self.full_clean()
        self.save()
        return self

class LoginError(models.Model):
    email = models.EmailField()
