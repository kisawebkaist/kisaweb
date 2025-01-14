from django import template
from django.utils.html import strip_tags

register = template.Library()

@register.filter
def seats_left(maximum, current):
    # "Registered/Seats left" text is used in registration AJAX request in event_registration.js
    if not maximum:
        return f'No limit'
    else:
        return f'{maximum - current} seats left'


@register.filter
def concatenate_eventid(str1, str2):
    return str(str1) + '#' + str(str2)


@register.simple_tag
def image_tag(event, listview=False):
    return event.image_tag(listview=listview)


@register.simple_tag
def edit_truncate_num_display(event):
    descr_no_tags = strip_tags(event.description)
    wordcount = len(descr_no_tags.split())
    min_num = event.min_descr_truncate_num
    if wordcount <= min_num:
        return 'none'
    else:
        return 'inline'

