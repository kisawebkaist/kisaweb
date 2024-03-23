import urllib.parse, string, secrets

from django.dispatch import Signal
from django.shortcuts import _get_queryset
from rest_framework.authentication import SessionAuthentication as DRFSessionAuthetication
from rest_framework.exceptions import NotFound

URLSAFE_CHARACTERS = string.ascii_letters + string.digits + '-_.~'
"""Reference: RFC 3986"""

class StrictCSRFSessionAuthentication(DRFSessionAuthetication):
    """
    Session authentication with csrf enforced for all requests
    """
    def authenticate(self, request):
        self.enforce_csrf(request)
        user = getattr(request._request, 'user', None)
        # Unauthenticated
        if (not user) or not user.is_active:
            return None
        return (user, None)
    
class CSRFExemptSessionAuthentication(DRFSessionAuthetication):
    """
    Session authentication without csrf
    """
    def enforce_csrf(self, request):
        pass

def ensure_relative_url(url):
    if url[0] == '/':
        return url
    url = urllib.parse.urlparse(url)._replace(scheme='', netloc='').geturl()
    if url == "" or url[0] != '/':
        url = '/' + url
    return url
    
def get_random_urlsafe_string(numchar):
    return ''.join(secrets.choice(URLSAFE_CHARACTERS) for i in range(numchar))

def get_object_or_404(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        raise NotFound

housekeeping_signal = Signal()
"""This signal will be sent frequently by cron to do some housekeeping"""