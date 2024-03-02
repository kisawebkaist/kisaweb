from django.contrib import admin
from .models import *

class MiscAdmin(admin.ModelAdmin):
    pass

admin.site.register(Misc, MiscAdmin)