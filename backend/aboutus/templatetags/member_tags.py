from django import template
from django.utils.html import strip_tags

register = template.Library()

@register.simple_tag
def image_tag(member, css_class=''):
    return member.image_tag(css_class=css_class)
