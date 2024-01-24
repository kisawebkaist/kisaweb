from django.apps import AppConfig
from django.conf import settings


class AuthmemConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "auth_mem"

    def ready(self):
        from .utils import GMailAPI
        if not settings.DEBUG:
            import logging
            logging.getLogger(__name__).info("Started GMailAPI.")
            GMailAPI.init()
        pass
