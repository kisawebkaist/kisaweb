import base64, json, logging, os, datetime
from django.core.exceptions import ImproperlyConfigured
from django.middleware.csrf import rotate_token
from django.utils.functional import SimpleLazyObject
from django.views.decorators.debug import sensitive_variables

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from .models import KAISTProfile

CAIS_AES_ID_SECRET = os.environ.get('KSSO_SECRET_KEY')
SA_AES_ID_SECRET = os.environ.get('KSSO_SECRET_KEY')

SESSION_KEY = 'kaist_profile'
CACHE_KEY = '_cached_kaist_profile'

logger = logging.getLogger(__name__)

def get_kaist_profile(request):
    if not hasattr(request, CACHE_KEY):
        session_key = request.session.get(SESSION_KEY)
        if session_key:
            request._cached_kaist_profile = KAISTProfile.objects.get(pk=int(session_key))
        elif request.user.is_authenticated:
            request._cached_kaist_profile = request.user.get_kaist_profile()
        else:
            request._cached_kaist_profile = KAISTAnonymousUser()
    return request._cached_kaist_profile

def decrypt(data, state) :
    BS = AES.block_size 
    key = (SA_AES_ID_SECRET+str(state))[80:96] # 128 bit
    iv=key[:16] # 128 bit
    cipher = AES.new(key.encode("utf8"), AES.MODE_CBC, IV=iv.encode("utf8"))
    deciphed = cipher.decrypt(base64.b64decode(data))   
    deciphed = unpad(deciphed, BS)
    return deciphed

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

@sensitive_variables("raw_result", "state")
def kauthenticate(request, raw_result, state):
    try:
        result = decrypt(raw_result, state).decode('utf-8')
        result = json.loads(result)
        user = KAISTProfile.from_info_json(result['dataMap']['USER_INFO'])
        user.last_login = datetime.datetime.now()
        user.full_clean()
        user.save()
        return user
    except:
        logging.exception(f'Login failed: (raw_result: {raw_result}, state: {state})')
        return None

def klogin(request, kaist_profile: KAISTProfile):
    if SESSION_KEY in request.session:
        session_key = int(request.session.get(SESSION_KEY))
        if session_key != kaist_profile.pk:
            request.session.flush()
    else:
        request.session.cycle_key()
    request.session[SESSION_KEY] = str(kaist_profile.pk)

    if hasattr(request, "kaist_profile"):
        request.kaist_profile = kaist_profile

    rotate_token(request)

def klogout(request):
    request.session.flush()
    request.kaist_profile = KAISTAnonymousUser()
