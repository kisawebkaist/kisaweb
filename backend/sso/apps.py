from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SsoConfig(AppConfig):
    name = "sso"
    verbose_name = _("KISA Authentication")