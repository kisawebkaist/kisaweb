import urllib, string, secrets

from rest_framework.authentication import SessionAuthentication as DRFSessionAuthetication

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
    try:
        return urllib.parse.urlparse(url)._replace(scheme='', netloc='').geturl()
    except:
        return '/'
    
def get_random_urlsafe_string(numchar):
    return ''.join(secrets.choice(URLSAFE_CHARACTERS) for i in range(numchar))