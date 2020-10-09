from django import template

register = template.Library()

@register.filter
def replace_space(string):
    return string.replace(' ', '-')
