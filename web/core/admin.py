from django.contrib import admin

from .models import Footer, Navbar

# Register your models here.

admin.site.site_header = 'KISA Web Administration'

admin.site.register(Footer)
admin.site.register(Navbar)
