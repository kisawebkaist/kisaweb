from django import forms
from django.contrib import admin

from web.admin import register, admin_site
from .models import *


admin_site.register(Semester)
@admin.register(Misc)
class MiscAdmin(admin.ModelAdmin):
    pass
