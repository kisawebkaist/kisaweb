from django.contrib import admin
from .models import UrlShortener
from .forms import UrlShortenerForm
from django.utils.safestring import mark_safe
from django import forms
from web.settings import URL_SHORTENER_PREFIX

# TODO: Fix this clutch
def get_main_website_url(full_url : str):
    urls    = full_url.split('/')
    main_url= ''
    for url in urls:
        if url != 'https:' and url != 'http:' and url != '':
            main_url    = url
            break
    return urls[0], main_url

# This builds the host url
def build_host(protocol : str, host_url : str):
    return f'{protocol}//{host_url}/{URL_SHORTENER_PREFIX}/'

# This builds the full url
def build_url(protocol : str, host_url : str, name : str):
    return f'{build_host(protocol, host_url)}{name}'

# Customized widget for Name to return the correct url
class NameWidget(forms.TextInput):
    def __init__(self, host_url : str):
        super().__init__()
        self.host_url   = host_url
    def render(self, *args, **kwargs):
        widget = mark_safe(self.host_url) + super().render(*args, **kwargs)
        return widget

@admin.register(UrlShortener)
class UrlShortenerAdmin(admin.ModelAdmin):
    list_display = ('shortened_link', 'target_link')
    form         = UrlShortenerForm

    # TODO: Factor this clutch for a better method
    def get_queryset(self, request):
        self.protocol, self.host_url    = get_main_website_url(
            request.build_absolute_uri()
        )
        return super().get_queryset(request)

    def shortened_link(self, obj : UrlShortener):
        return build_url(self.protocol, self.host_url, obj.name)

    def target_link(self, obj : UrlShortener):
        return obj.target

    def formfield_for_dbfield(self, db_field, **kwargs):
        host_url    = build_host(self.protocol, self.host_url)
        if db_field.name == 'name':
            # You could put following customized widget elsewhere
            kwargs['widget']= NameWidget(host_url)
        return super().formfield_for_dbfield(db_field, **kwargs)


