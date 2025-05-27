from django.contrib import admin

from web.admin import admin_site
from .models import *
# Register your models here.
admin_site.register(KISA_Position)
admin_site.register(Alumni)