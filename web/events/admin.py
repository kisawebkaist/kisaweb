from django.contrib import admin
from django.utils.html import mark_safe
from django import forms

from .models import Event

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'event_start_datetime',
        'event_end_datetime',
        'registration_start_datetime',
        'registration_end_datetime',
        'image_tag',
    ]

    def image_tag(self, obj):
        if not obj.image:
            path = '/static/img/events-default-dev-dist.png'
        else:
            path = obj.image.url
        return mark_safe(f'<img src="{path}" alt="Event Image" width="150" height="150" />')

    image_tag.short_description = 'Current Image'
    readonly_fields = ['image_tag', 'participants']


admin.site.register(Event, EventAdmin)
