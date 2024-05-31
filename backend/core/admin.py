from django import forms
from django.contrib import admin
from django.contrib.admin.forms import AdminAuthenticationForm
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy
from django.views.decorators.cache import never_cache

from .models import *

class CustomAuthenticationForm(AdminAuthenticationForm):

    def clean(self):
        return super().clean()

class TwoFAForm(forms.Form):
    token = forms.CharField(
        label="OTP",
        max_length=6,
        min_length=6,
        required=True,
        widget=forms.TextInput()
    )


class CustomAdminSite(admin.AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = gettext_lazy("KISA Admin")

    # Text to put in each page's <h1>.
    site_header = gettext_lazy("KISA Website Administration")

    # Text to put at the top of the admin index page.
    index_title = gettext_lazy("Site administration")

    login_form = CustomAuthenticationForm
    login_template = "admin/login_custom.html"

    two_fa_form = TwoFAForm

    def has_permission(self, request):
        return super().has_permission(request) and (not request.user.totp_device.is_active or request.user.is_verified(request))
    
    @method_decorator(never_cache)
    def login(self, request, extra_context=None):
        shown_username = "anonymous" if request.user.is_anonymous else request.user.email
        context = {
            "2fa_path": reverse("check-otp"),
            "sso_login_path": reverse("login"),
            "2fa_form": self.two_fa_form,

            "is_authenticated": request.user.is_authenticated,
            "need_2fa": request.user.is_authenticated and request.user.totp_device.is_active and not request.user.is_verified(request),
            "username": shown_username
        }
        context.update(extra_context or {})
        return super().login(request, extra_context=context)

site = CustomAdminSite(name="KISA Admin")

def register(*models):
    def _wrapper(admin_class):
        site.register(models, admin_class=admin_class)
        return admin_class
    return _wrapper

@register(Misc)
class MiscAdmin(admin.ModelAdmin):
    pass
