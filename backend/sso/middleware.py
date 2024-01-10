from django.core.exceptions import ImproperlyConfigured
from django.middleware.csrf import rotate_token
from django.utils.functional import SimpleLazyObject

from .models import KAISTProfile

SESSION_KEY = 'kaist_profile'

def get_kaist_profile(request):
    if not hasattr(request, '_cached_kaist_profile'):
        session_key = request.session.get(SESSION_KEY)
        if session_key:
            request._cached_kaist_profile = KAISTProfile.objects.get(pk=int(session_key))
        elif request.user.is_authenticated:
            request._cached_kaist_profile = request.user.get_kaist_profile()
        else:
            request._cached_kaist_profile = KAISTAnonymousUser()
    return request._cached_kaist_profile

class KAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if not hasattr(request, "session"):
            raise ImproperlyConfigured(
                "KAuthMiddleware requires session middleware to be installed."
            )
        if not hasattr(request, "user"):
            raise ImproperlyConfigured(
                "KAuthMiddleware requires auth middleware to be installed"
            )
        
        request.kaist_profile = SimpleLazyObject(lambda: get_kaist_profile(request))
        return self.get_response(request)
        

class KAISTAnonymousUser:
    is_authenticated = False

def klogin(request, kaist_profile: KAISTProfile):
    if SESSION_KEY in request.session:
        session_key = int(request.session.get(SESSION_KEY))
        if session_key != kaist_profile.pk:
            request.session.flush()
    else:
        request.session.cycle_key()
    request.session[SESSION_KEY] = str(kaist_profile.pk)
    print(request.session[SESSION_KEY])
    rotate_token(request)

def klogout(request):
    request.session.flush()
    request.user = KAISTAnonymousUser()