from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from django.urls import reverse

class CustomSessionMiddleware(SessionMiddleware):
    """
    This session middleware overrides the behaviour of `SessionMiddleware` to set the session cookie to samesite=None for anonymous users
    """
    def process_response(self, request: HttpRequest, response: HttpResponse) -> HttpResponse:
        super_response = super().process_response(request, response)
        if settings.SESSION_COOKIE_NAME in super_response.cookies and request.user.is_anonymous:
            super_response.cookies[settings.SESSION_COOKIE_NAME]['samesite'] = 'None'
            if not settings.DEBUG:
                super_response.cookies[settings.SESSION_COOKIE_NAME]['secure'] = True
        return super_response