from rest_framework.throttling import SimpleRateThrottle
from rest_framework.throttling import ScopedRateThrottle as DRFScopedRateThrottle

class KAISTProfileRateThrottle(SimpleRateThrottle):
    scope = 'kaist'

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            return None
        elif request.kaist_profile and request.kaist_profile.is_authenticated:
            indent = 'k_' + str(request.kaist_profile.pk)
        else:
            indent = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'indent': indent
        }
    
class ScopedRateThrottle(DRFScopedRateThrottle):
    """
    According to this setup, actually members have 
    - maximum throttle = kaist user throttle + member throttle
    """
    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            ident = 'm_' + str(request.user.pk)
        elif request.kaist_profile and request.kaist_profile.is_authenticated:
            ident = 'k_' + str(request.kaist_profile.pk)
        else:
            self.get_ident(request)
        
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
    