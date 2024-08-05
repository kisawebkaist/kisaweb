from django.contrib import admin
from django.utils.html import mark_safe
from django import forms

from django_draftjs import EditorWidget

from core.admin import register
from .models import Event
# from .forms import EventForm

class EventForm(forms.ModelForm):
    description = forms.JSONField(widget= EditorWidget())
    class Meta: 
        model = Event
        fields = '__all__'

@register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'event_start_datetime']
    form = EventForm