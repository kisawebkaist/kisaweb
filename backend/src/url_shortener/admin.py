from typing import Tuple
from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from django.utils.html import linebreaks, format_html
from web.settings import URL_SHORTENER_PREFIX

from core.admin import register
from .forms import UrlShortenerForm
from .models import UrlShortener, UrlVisitor

# TODO: Fix this clutch
def get_main_website_url(full_url : str) -> Tuple[str, str]:
    urls    = full_url.split('/')
    main_url= ''
    for url in urls:
        if url != 'https:' and url != 'http:' and url != '':
            main_url    = url
            break
    return urls[0], main_url

# This builds the host url
def build_host(protocol : str, host_url : str) -> str:
    return f'{protocol}//{host_url}/{URL_SHORTENER_PREFIX}/'

# This builds the full url
def build_url(host_url : str, name : str) -> str:
    return f'{host_url}{name}'

# Customized widget for Name to return the correct url
class NameWidget(forms.TextInput):
    def __init__(self, host_url : str):
        super().__init__()
        self.host_url   = host_url
    def render(self, *args, **kwargs):
        widget = mark_safe(self.host_url) + super().render(*args, **kwargs)
        return widget

@register(UrlShortener)
class UrlShortenerAdmin(admin.ModelAdmin):
    list_display = (
        'shortened_link', 'target_link', 'visitor_count', 'total_visit'
    )
    form         = UrlShortenerForm

    # TODO: Factor this clutch for a better method
    def get_queryset(self, request):
        self.host_url = build_host(*get_main_website_url(
            request.build_absolute_uri()
        ))
        return super().get_queryset(request)

    def total_visit(self, obj : UrlShortener):
        return obj.total_visits()

    def shortened_link(self, obj : UrlShortener):
        return build_url(self.host_url, obj.name)

    def target_link(self, obj : UrlShortener):
        return obj.target

    def visitor_count(self, obj : UrlShortener):
        return obj.visitor_count()

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'name':
            # You could put following customized widget elsewhere
            kwargs['widget']= NameWidget(self.host_url)
        return super().formfield_for_dbfield(db_field, **kwargs)

@register(UrlVisitor)
class UrlVisitorAdmin(admin.ModelAdmin):
    list_display = ('visitor', 'visited_links_and_count')
    def get_queryset(self, request):
        self.host_url = build_host(*get_main_website_url(
            request.build_absolute_uri()
        ))
        return super().get_queryset(request)

    def visitor(self, obj : UrlVisitor):
        return obj.ip_address

    def visited_links_and_count(self, obj : UrlVisitor):
        links   = obj.visited_links_and_count()
        return format_html(linebreaks('\n\n'.join([
            'Link  : ' + build_url(self.host_url, link['name']) \
            + f'\nCount : {link["visit_count"]}' for link in links
        ])))

