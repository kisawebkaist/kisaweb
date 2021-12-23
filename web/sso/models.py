from django.db import models
from django.contrib.auth.models import AbstractUser

from tinymce.models import HTMLField

# Create your models here.


class User(AbstractUser):
    class Meta:
        permissions = [
            ('see_election_results', 'Can view election results anytime')
        ]
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

class LoginError(models.Model):
    email = models.EmailField()
