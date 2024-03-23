from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

class MailOTPSessionAdmin(admin.ModelAdmin):
    pass

class TOTPDeviceAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(MailOTPSession, MailOTPSessionAdmin)
admin.site.register(TOTPDevice, TOTPDeviceAdmin)