from django.db import models
from django.utils.html import mark_safe
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify

from tinymce.models import HTMLField

from web.settings import BASE_DIR


# Create your models here.


class Question(models.Model):
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    faq = models.BooleanField()
    faq_answer = models.TextField(null=True, blank=True)


class Answer(models.Model):
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

