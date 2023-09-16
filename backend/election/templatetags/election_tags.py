from django import template
from django.utils import timezone as tz
from django.utils import dateformat

from election.models import Election

register = template.Library()

@register.filter
def replace_space(string):
    return string.replace(' ', '-')

@register.filter
def to_int(value):
    return int(dateformat.format(value, 'YmdHis'))

@register.simple_tag
def voting_time():
    try:
        e = Election.objects.latest('start_datetime')
    except Election.DoesNotExist:
        e = None
    if e:
        st = int(dateformat.format(tz.now(), 'YmdHis')) >= int(dateformat.format(e.start_datetime, 'YmdHis'))
        et = int(dateformat.format(tz.now(), 'YmdHis')) <= int(dateformat.format(e.end_datetime, 'YmdHis'))
        if st and et:
            return True
    return None
