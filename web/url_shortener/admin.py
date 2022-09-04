from django.contrib import admin
from .models import UrlShortener
from .forms import UrlShortenerForm
from django.utils.safestring import mark_safe
from django import forms

def get_main_website_url(full_url : str):
    urls    = full_url.split('/')
    main_url= ''
    for url in urls:
        if url != 'https:' and url != 'http:' and url != '':
            main_url    = url
            break
    return main_url

def build_url(host_url : str, name : str):
    return f'https://{host_url}/short-link/{name}'

@admin.register(UrlShortener)
class UrlShortenerAdmin(admin.ModelAdmin):
    list_display = ('shortened_link', 'target_link')
    form         = UrlShortenerForm

    # TODO: Factor this clutch for a better method
    def get_queryset(self, request):
        self.host_url    = get_main_website_url(
            request.build_absolute_uri()
        )
        return super().get_queryset(request)

    def shortened_link(self, obj : UrlShortener):
        return build_url(self.host_url, obj.name)

    def target_link(self, obj : UrlShortener):
        return obj.target

    def formfield_for_dbfield(self, db_field, **kwargs):
        host_url    = f'https://{self.host_url}/short-link/'
        if db_field.name == 'name':
            # You could put following customized widget elsewhere
            class Widget(forms.TextInput):
                def render(self, *args, **kwargs):
                    return mark_safe(host_url) +\
                    super().render(*args, **kwargs)
            kwargs['widget']= Widget()
        return super().formfield_for_dbfield(db_field, **kwargs)


