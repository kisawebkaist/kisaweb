from django.db import models

from tinymce.models import HTMLField

# Create your models here.


class Agreement(models.Model):
    english = HTMLField()
    korean = HTMLField()


class LoginError(models.Model):
    email = models.EmailField()
