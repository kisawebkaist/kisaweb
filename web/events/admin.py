from django.contrib import admin
from django.utils.html import mark_safe
from django import forms

from .models import Event
# from .forms import EventForm

# Register your models here.


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # form = EventForm
    # add_form_template = 'admin/crispy_form.html'
    list_display = [
        'title',
        'event_start_datetime',
        'event_end_datetime',
        'registration_start_datetime',
        'registration_end_datetime',
        'image_tag',
    ]

    # fields = [
    #     'title',
    #     'is_link',
    #     ('location', 'link'),
    #     # ('event_start_datetime', 'event_end_datetime'),
    #     'event_start_datetime',
    # ]

    def image_tag(self, obj):
        if not obj.image:
            path = '/static/img/events-default-dev-dist.png'
        else:
            path = obj.image.url
        return mark_safe(f'<img src="{path}" alt="Event Image" width="150" height="150" />')

    image_tag.short_description = 'Current Image'
    readonly_fields = ['image_tag', 'participants']
