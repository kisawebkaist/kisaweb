import os, logging, secrets, urllib.parse

from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.utils.translation import gettext as _

from rest_framework.decorators import api_view, parser_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import FormParser
import rest_framework.status as status

from .middleware import klogin, klogout, kauthenticate
from core.exceptions import IncorrectEndpointException

KSSO_LOGIN_URL = os.environ.get('KSSO_LOGIN_URL')
KSSO_LOGOUT_URL = os.environ.get('KSSO_LOGOUT_URL')
KSSO_CLIENT_ID = os.environ.get('KSSO_CLIENT_ID')

KSSO_SITE = f'https://{urllib.parse.urlparse(KSSO_LOGIN_URL).netloc}'

logger = logging.getLogger(__name__)

def ensure_relative_url(url):
    if url[0] == '/':
        return url
    try:
        return urllib.parse.urlparse(url)._replace(scheme='', netloc='').geturl()
    except:
        return '/'

@api_view(['POST'])
def login_view(request):
    """
    Format
    ------
    {'next': <the url to be redirected after login>}

    For Frontend
    ------------
    - Make a post request and follow the redirect

    Here, since the redirect endpoint is at the backend-side, it will take the responsibility for redirect
    """
    next = request.data.get('next', '/')

    if request.kaist_profile.is_authenticated or request.user.is_authenticated:
        return HttpResponseRedirect(ensure_relative_url(next))

    if request.session.get('state') is None:
        state = secrets.token_hex(16)
        request.session['state'] = state
        request.session['next'] = ensure_relative_url(next)
    else:
        state = request.session['state']

    data = {
        'client_id': KSSO_CLIENT_ID,
        'redirect_url': request.build_absolute_uri(reverse('klogin-response')),
        'state': state,
    }
    return HttpResponseRedirect(f"{KSSO_LOGIN_URL}?{urllib.parse.urlencode(data)}")

@api_view(['POST'])
@parser_classes([FormParser])
@csrf_exempt
def login_response_view(request):
    """
    This POST request is supposed to be sent by sso website and contains encrypted user information.
    This view is csrf_exempted but we will enforce strict origin-checking manually.
    We also need to allow cors from sso website with credentials.
    """
    state = request.data.get('state', '0'*16)
    raw_result = request.data.get('result', '')
    success = request.data.get('success', '')
    origin = request.META.get('HTTP_ORIGIN')

    headers = {
        'Access-Control-Allow-Origin': KSSO_SITE,
        'Access-Control-Allow-Credentials': 'true'
    }

    if not origin == KSSO_SITE:
        logger.info(f"Invalid \"Origin\" header: {origin} in login-response (state: {state}, raw_result:{raw_result}, user-agent: {request.META.get('HTTP_USER_AGENT')})")
        # the response won't even be readable in a browser unless it comes from the same origin
        raise PermissionDenied(detail=_(f'This page requires that "Origin" header to be "{KSSO_SITE}" to prevent cross-subdomain csrf.'))
    
    if request.kaist_profile.is_authenticated or request.user.is_authenticated:
        return HttpResponseRedirect(next, headers=headers)

    
    # TODO: to find out if bool is even the right function to use here
    if not bool(success):
        return JsonResponse(
            {'detail': _('Login failed.')}, 
            headers = headers,
            status = status.HTTP_400_BAD_REQUEST
            )

    saved_state = request.session.get('state')
    del request.session['state']
    
    if saved_state is None or saved_state != state:
        raise PermissionDenied(detail=_("Incorrect credentials provided."))
    
    user = kauthenticate(request, raw_result, state)
    if user is None:
        raise PermissionDenied(detail=_("Incorrect credentials provided."))
    
    klogin(request, user)

    next = request.session.get('next', '/')
    del request.session['next']
    return HttpResponseRedirect(next, headers)



@api_view(['POST'])
def logout_view(request):
    """
    Format
    ------
    {'next': <the url to be redirected to after logout>}
    
    For Frontend
    ------------
    - Make a post request and follow the redirect
    """
    if request.user.is_authenticated:
        raise IncorrectEndpointException(detail="Use the other endpoint to logout.")

    klogout(request)
    
    next = ensure_relative_url(request.data.get('next', '/'))
    
    data = {
        'client_id': KSSO_CLIENT_ID,
        'redirect_url': request.build_absolute_uri(next),
    }

    return HttpResponseRedirect(f"{KSSO_LOGOUT_URL}?{urllib.parse.urlencode(data)}")
