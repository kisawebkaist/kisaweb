import urllib

from rest_framework.authentication import SessionAuthentication as DRFSessionAuthetication

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
    try:
        return urllib.parse.urlparse(url)._replace(scheme='', netloc='').geturl()
    except:
        return '/'