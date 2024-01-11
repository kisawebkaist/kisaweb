import os, logging, secrets, urllib.parse

from django.http.response import HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest

from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect

from .middleware import klogin, klogout, kauthenticate

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext as _

KSSO_LOGIN_URL = os.environ.get('KSSO_LOGIN_URL')
KSSO_LOGOUT_URL = os.environ.get('KSSO_LOGOUT_URL')
KSSO_CLIENT_ID = os.environ.get('KSSO_CLIENT_ID')

logger = logging.getLogger(__name__)

def ensure_relative_url(url):
    if url[0] == '/':
        return url
    try:
        return urllib.parse.urlparse(url)._replace(scheme='', netloc='').geturl()
    except:
        return '/'
    

@require_http_methods(['POST'])
def login_view(request):
    next = request.POST.get('next', '/')

    if request.kaist_profile.is_authenticated or request.user.is_authenticated:
        return HttpResponseRedirect(ensure_relative_url(next))

    if request.session.get('state') is None:
        state = secrets.token_hex(16)
        request.session['state'] = state
    else:
        state = request.session['state']

    data = {
        'client_id': KSSO_CLIENT_ID,
        'redirect_url': request.build_absolute_uri(reverse('klogin-response')) + '?next=' + urllib.parse.quote_plus(next),
        'state': state,
    }
    return HttpResponseRedirect(f"{KSSO_LOGIN_URL}?{urllib.parse.urlencode(data)}")

@require_http_methods(['POST'])
@csrf_exempt
def login_response_view(request):
    """
    This POST request is supposed to be sent by sso website and contains encrypted user information.
    """

    next = ensure_relative_url(request.POST.get('next', '/'))
    state = request.POST.get('state', '0'*16)
    raw_result = request.POST.get('result', '')
    success = request.POST.get('success')
    origin = request.META.get('HTTP_ORIGIN')


    if not origin == 'https://iam2.kaist.ac.kr':
        logger.info(f"Invalid \"Origin\" header: {origin} in login-response (state: {state}, raw_result:{raw_result}, user-agent: {request.META.get('HTTP_USER_AGENT')})")
        return HttpResponseForbidden(_(f'This page requires that "Origin" header to be "https://iam2.kaist.ac.kr" to prevent cross-subdomain <a href="https://en.wikipedia.org/wiki/Cross-site_request_forgery">CSRF,s</a>.'))
    
    if request.kaist_profile.is_authenticated or request.user.is_authenticated:
        return HttpResponseRedirect(next)

    # TODO: to find out if bool is even the right function to use here
    if not bool(success):
        return redirect('klogin-error')

    saved_state = request.session.get('state')
    del request.session['state']
    
    if saved_state is None or saved_state != state:
        return redirect('klogin-error')
    
    user = kauthenticate(request, raw_result, state)
    if user is None:
        return redirect('klogin-error')
    
    klogin(request, user)
    return HttpResponseRedirect(ensure_relative_url(next))


def login_error_view(request):
    return render(request, 'sso/login_error.html', {})


@require_http_methods(['POST'])
def logout_view(request):
    next = ensure_relative_url(request.POST.get('next', '/'))

    if request.user.is_authenticated:
        return HttpResponseBadRequest()

    if not request.kaist_profile.is_authenticated:
        return HttpResponseRedirect(next)

    klogout(request)
    
    data = {
        'client_id': KSSO_CLIENT_ID,
        'redirect_url': request.build_absolute_uri(next),
    }

    return HttpResponseRedirect(f"{KSSO_LOGOUT_URL}?{urllib.parse.urlencode(data)}")
