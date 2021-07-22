from django.contrib import admin
from django.utils.html import mark_safe
from django import forms

from .models import Question
# from .forms import EventForm
from .models import Category

# Register your models here.

admin.site.register(Question)
admin.site.register(Category)
