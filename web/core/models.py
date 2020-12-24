from django.db import models
from django.core.exceptions import ValidationError

from phone_field import PhoneField

# Create your models here.

class Footer(models.Model):
    kisa_text = models.CharField(max_length=500, blank=True)

    location = models.CharField(max_length=80, blank=False)
    phnum_eng = PhoneField(blank=False)
    phnum_kor = PhoneField(blank=False)
    email = models.EmailField(max_length=20, blank=False)

    fb_link = models.URLField(blank=True)
    insta_link = models.URLField(blank=True)
    yt_link = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        # if you'll not check for self.pk
        # then error will also raised in update of exists model
        if not self.pk and Footer.objects.all():
            raise ValidationError('There is can be only one Footer instance')
        return super().save(*args, **kwargs)


class EmptyQueryset(models.Model):
    events = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        # if you'll not check for self.pk
        # then error will also raised in update of exists model
        if not self.pk and EmptyQueryset.objects.all():
            raise ValidationError('There is can be only one EmptyQueryset instance')
        return super().save(*args, **kwargs)


class CourseResources(models.Model):
    class_id = models.CharField(max_length=255, unique=True)
    class_name = models.CharField(max_length=255)
    url = models.CharField(max_length=512, blank=True)

