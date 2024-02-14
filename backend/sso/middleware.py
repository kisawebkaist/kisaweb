import base64, json, logging, os, datetime
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import SimpleLazyObject

SESSION_KEY = '_totp_verified'

logger = logging.getLogger(__name__)

class OTPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if not hasattr(request, "session"):
            raise ImproperlyConfigured(
                "OTPMiddleware requires session middleware to be installed."
            )
        if not hasattr(request, "user"):
            raise ImproperlyConfigured(
                "OTPMiddleware requires auth middleware to be installed"
            )
        request.user.is_verified = SESSION_KEY in request.session and bool(request.session[SESSION_KEY])
        
        response = self.get_response(request)

        if hasattr(request.user, "is_verified") and request.user.is_verified:
            request.session[SESSION_KEY] = True
        else:
            request.session.pop(SESSION_KEY, None)

        return response
        