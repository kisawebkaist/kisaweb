from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from election.models import DebateAttendance, Election
from core.admin import register, site
from .models import *

class KISADivisionFilter(admin.SimpleListFilter):
    title = _('KISA Divsion')
    parameter_name = 'kisa_division'

    def lookups(self, request, model_admin):
        return list(zip(KISADivision.names, KISADivision.labels))+[
            ("KISA", _("All KISA"))
        ]
    
    def queryset(self, request, queryset):
        value = self.value()
        if value == "KISA":
            return queryset.exclude(kisa_division=KISADivision.NONE)
        if value in KISADivision.names:
            return queryset.filter(kisa_division=KISADivision.names.index(value))
        
@admin.action(description="Create DebateAttendance for selected users")
def create_debate_attendance(modeladmin, request, queryset):
    election = Election.current_or_error()
    DebateAttendance.objects.bulk_create([
        DebateAttendance(user=user, election=election) for user in queryset
    ])

@register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ["name", "email", "is_staff", "kisa_division"]
    list_filter = ["is_staff", "is_superuser", KISADivisionFilter, "groups"]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "kisa_division", "student_number")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    readonly_fields = [
        "username",
        "student_number"
    ]
    actions = [create_debate_attendance]
    def name(self, obj):
        return f"{obj.last_name},{obj.first_name} ({obj.username})"
    

@register(MailOTPSession)
class MailOTPSessionAdmin(admin.ModelAdmin):
    pass

@register(TOTPDevice)
class TOTPDeviceAdmin(admin.ModelAdmin):
    pass
