import base64, json, os, logging, secrets, urllib.parse

from django.http.response import HttpResponseRedirect, HttpResponseForbidden
from web.settings import SECRET_KEY

from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect

from .models import KAISTProfile
from .middleware import klogin, klogout

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext as _

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

KSSO_LOGIN_URL = os.environ.get('KSSO_LOGIN_URL')
KSSO_LOGOUT_URL = os.environ.get('KSSO_LOGOUT_URL')

KSSO_CLIENT_ID = os.environ.get('KSSO_CLIENT_ID')

CAIS_AES_ID_SECRET = os.environ.get('KSSO_SECRET_KEY')
SA_AES_ID_SECRET = os.environ.get('KSSO_SECRET_KEY')


logger = logging.getLogger(__name__)

def ensure_relative_url(url):
    if url[0] == '/':
        return url
    try:
        return urllib.parse.urlparse(url)._replace(scheme='', netloc='').geturl()
    except:
        return '/'
    
    
def decrypt(data, state, host) :
    BS = AES.block_size 
    if host in ('ka', 'co','ca') :
        key = (CAIS_AES_ID_SECRET+str(state))[80:96] # 128 bit
    else :
        key = (SA_AES_ID_SECRET+str(state))[80:96] # 128 bit
    iv=key[:16] # 128 bit
    cipher = AES.new(key.encode("utf8"), AES.MODE_CBC, IV=iv.encode("utf8"))
    deciphed = cipher.decrypt(base64.b64decode(data))   
    deciphed = unpad(deciphed, BS)
    return deciphed

@require_http_methods(['POST'])
def login_view(request):
    next = request.POST.get('next', '/')

    if request.kaist_profile.is_authenticated:
        return HttpResponseRedirect(ensure_relative_url(next))

    if request.session.get('state') is None:
        state = secrets.token_hex(16)
        request.session['state'] = state
    else:
        state = request.session['state']

    data = {
        'client_id': KSSO_CLIENT_ID,
        'redirect_url': request.build_absolute_uri(reverse('login-response')) + '?next=' + urllib.parse.quote_plus(next),
        'state': state,
    }
    return HttpResponseRedirect(f"{KSSO_LOGIN_URL}?{urllib.parse.urlencode(data)}")

@require_http_methods(['POST'])
@csrf_exempt
def login_response_view(request):
    next = ensure_relative_url(request.POST.get('next', '/'))
    state = request.POST.get('state', '0'*16)
    raw_result = request.POST.get('result', '')
    success = request.POST.get('success')
    http_host = request.META.get('HTTP_HOST') # host header validation is already done by middleware
    origin = request.META.get('HTTP_ORIGIN')


    if not origin == 'https://iam2.kaist.ac.kr':
        logger.info(f"Invalid \"Origin\" header: {origin} in login-response (state: {state}, raw_result:{raw_result}, user-agent: {request.META.get('HTTP_USER_AGENT')})")
        return HttpResponseForbidden(_(f'This page requires that "Origin" header to be "https://iam2.kaist.ac.kr" to prevent cross-subdomain <a href="https://en.wikipedia.org/wiki/Cross-site_request_forgery">CSRF,s</a>.'))
    
    if request.kaist_profile.is_authenticated:
        return HttpResponseRedirect(next)

    # TODO: to find out if bool is even the right function to use here
    if not bool(success):
        return redirect('login-error')

    saved_state = request.session.get('state')
    del request.session['state']
    
    if saved_state is None or saved_state != state:
        return redirect('login-error')
    
    try:
        result = decrypt(raw_result, state, http_host[:2]).decode('utf-8')
        result = json.loads(result)

        user_info = result['dataMap']['USER_INFO']
        user = KAISTProfile.from_info_json(user_info)
        user.full_clean()
        user.save()

        klogin(request, user)

        return HttpResponseRedirect(ensure_relative_url(next))
    
    except Exception as e:
        logger.exception(f'An exception occurred in login-respon se while processing result. (state: {state}, raw_result: {result})')
        return redirect('login-error')


def login_error_view(request):
    return render(request, 'sso/login_error.html', {})


@require_http_methods(['POST'])
def logout_view(request):
    next = ensure_relative_url(request.POST.get('next', '/'))

    if not request.kaist_profile.is_authenticated:
        return HttpResponseRedirect(next)

    klogout(request)
    
    data = {
        'client_id': KSSO_CLIENT_ID,
        'redirect_url': request.build_absolute_uri(next),
    }

    return HttpResponseRedirect(f"{KSSO_LOGOUT_URL}?{urllib.parse.urlencode(data)}")
