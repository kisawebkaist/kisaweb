from django.db import models
from django.utils.html import mark_safe
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify

from tinymce.models import HTMLField

from web.settings import BASE_DIR


# Create your models here.
'''
CATEGORY = (
    ("", "---"),
    ("Student life", "Student"),
    ("Academics", "Academics"),
    ("Advices", "Advices"),
    ("nothing", "nothing"),
)
'''
class Category(models.Model):
   tittle_category = models.CharField( max_length= 200, blank=True)

class Question(models.Model):
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    faq = models.BooleanField()
    '''
    category = models.CharField(
        max_length=20,
        choices=CATEGORY,
        default='nothing'
    )
    '''
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    faq_answer = models.TextField(null=True, blank=True)


class Answer(models.Model):
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

