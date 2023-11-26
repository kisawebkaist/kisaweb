from django.shortcuts import HttpResponse
from django.utils.html import mark_safe

import yaml

from .models import EmptyQueryset
from web.settings import KISA_AUTH_METHOD, LOGIN_DEV, LOGIN_PROD


def string_adder(text: str, add_string: str, line_len: int) -> str:
    if not text:
        return ''

    lst = text.split()
    lines = []
    line = ''
    length = 0

    for word in lst:
        length += len(word) + 1  # '+1' for the space
        if length > line_len:
            lines.append(line)
            line = ''
            length = 0
        line += word + ' '

    return '\n'.join(lines)


# def footer(request):
#     if Footer.objects.all().exists():
#         footer_ = Footer.objects.all()[0]
#     else:
#         f = open('data/required.yaml')
#         parsed = yaml.safe_load(f)
#         data = next((d for d in parsed if d['model']=='core.models.Footer'))['fields']
#         footer_ = Footer.objects.create(**data)
#         f.close()

#     br_tag = '<br class="d-none d-xl-block" />'
#     line_len = 70
#     kisa_text = string_adder(footer_.kisa_text, br_tag, line_len)

#     return {
#         'footer': footer_,
#         'kisa_text': kisa_text,
#     }


# def navbar(request):
#     if Navbar.objects.all().exists():
#         navbar_ = Navbar.objects.all()[0]
#     else:
#         f = open('data/required.yaml')
#         parsed = yaml.safe_load(f)
#         data = next((d for d in parsed if d['model']=='core.models.Navbar'))['fields']
#         navbar_ = Navbar.objects.create(**data)
#         f.close()

#     return {'navbar': navbar_}


def empty_queryset(request):
    empty = EmptyQueryset.objects.all()
    return {
        'empty': empty,
    }


def login_type(request):
    return {
        'authmethod': KISA_AUTH_METHOD,
        'logindev': LOGIN_DEV,
        'loginprod': LOGIN_PROD,
    }
