import base64, datetime, time, json, logging, urllib.parse, pyotp, requests, secrets

from corsheaders.signals import check_request_enabled

from django.conf import settings
from django.contrib.auth import login, logout
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.signing import BadSignature, SignatureExpired
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.crypto import constant_time_compare
from django.utils.translation import gettext as _
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes, throttle_classes
from rest_framework.exceptions import PermissionDenied, ParseError, ValidationError, Throttled
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import rest_framework.status as status

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from . import TOTP_SESSION_KEY
from .models import User, MailOTPSession
from .permissions import IsKISA, IsVerified
from core.utils import ensure_relative_url, get_random_urlsafe_string, CSRFExemptSessionAuthentication
from core.throttling import EMAILOTPRateThrottle

MAIL_OTP_BASE_SESSION_KEY = "_mail_otp_" 

logger = logging.getLogger(__name__)
email_validator = EmailValidator()

# check https://datatracker.ietf.org/doc/html/rfc6749#section-10, https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics 
    
@api_view(['POST'])
@ensure_csrf_cookie
def login_init_view(request):
    """
    Nonce
        - check https://openid.net/specs/openid-authentication-2_0.html#verify_nonce
        - nonce binds the authorization request to the info response preventing the replay attacks

    State
        - check https://datatracker.ietf.org/doc/html/rfc6749#section-10.12
        - state prevents the attacker from abusing the redirection uri
    """
    if request.user.is_authenticated:
        return Response({
            'is_authenticated': True,
            'data': None
        })
    
    nonce = base64.urlsafe_b64encode(int(time.time()).to_bytes(8, byteorder='big') + secrets.token_bytes(16)).decode()
    state = base64.urlsafe_b64encode(secrets.token_bytes(16)).decode()

    request.session['login_nonce'] = nonce
    request.session['login_state'] = state
 
    return Response({
        'is_authenticated': False,
        'data': {
            'payload': {
                'response_type': 'code',
                'scope': 'openid',
                'client_id': settings.KSSO_CLIENT_ID,
                'redirect_uri': settings.KSSO_REDIRECT_URI,
                'state': state,
                'nonce': nonce,
            },
            'auth_uri': settings.KSSO_AUTH_REQUEST_URI
        }
    })
    

@api_view(['POST'])
@parser_classes([FormParser])
@authentication_classes([CSRFExemptSessionAuthentication])
def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    
    code = request.data['code']
    agent_state = request.data['state']
    
    # to avoid brute-force attacks
    state = request.session.pop('login_state', '')
    nonce = request.session.pop('login_nonce', '')

    # if the 'Origin' header exists, it must be from the sso website
    print(request.headers)
    print(request.headers.get('Origin', 'https://sso.kaist.ac.kr'))
    if request.headers.get('Origin', 'https://sso.kaist.ac.kr') != 'https://sso.kaist.ac.kr':
        raise PermissionDenied(detail=_('Invalid origin'))
    
    print(state, agent_state)
    if not constant_time_compare(state, agent_state):
        raise PermissionDenied(detail=_('Invalid state'))
    

    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.KSSO_REDIRECT_URI,
        'client_id': settings.KSSO_CLIENT_ID,
        'client_secret': settings.KSSO_CLIENT_SECRET,
    }

    response = requests.post(settings.KSSO_INFO_REQUEST_URI, payload).json()
    if not constant_time_compare(nonce, response['nonce']):
        raise PermissionDenied(detail=_('Invalid nonce'))
    user = User.from_info_json(response['userInfo'])
    login(request, user)
    request.session.pop(TOTP_SESSION_KEY, None)
    return HttpResponseRedirect('https://kisa.kaist.ac.kr:8080/')

@api_view(['POST'])
@permission_classes([IsKISA])
def check_totp_view(request):
    if request.user.totp_device.verify(str(request.data.get('token', ''))):
        request.session.cycle_key()
        request.session[TOTP_SESSION_KEY] = True
    else: 
        raise ParseError()
    return Response({
        "redirect": ensure_relative_url(str(request.data.get('next', '/')))
    })

@api_view(['POST'])
@permission_classes([IsVerified])
def change_totp_secret(request):
    new_secret = pyotp.random_base32()
    request.user.totp_device.secret = new_secret
    request.user.totp_device.save()
    return Response({
        "secret": new_secret,
        "auth_uri": pyotp.TOTP(new_secret).provisioning_uri(name=request.user.email, issuer_name="KISA")
    })


@api_view(['POST'])
@permission_classes([IsVerified])
@throttle_classes([EMAILOTPRateThrottle])
def change_email_view(request):
    if MAIL_OTP_BASE_SESSION_KEY+'change_mail_cooldown' in request.session and datetime.datetime.fromtimestamp(request.session[MAIL_OTP_BASE_SESSION_KEY+'change_mail_cooldown']) > datetime.datetime.now():
        raise Throttled()
    request.session[MAIL_OTP_BASE_SESSION_KEY+'change_mail_cooldown'] = (datetime.datetime.now() + datetime.timedelta(minutes=2)).timestamp()
    request.session.save()
    email = str(request.data.get('email', ''))
    try:
        email_validator(email)
        email = User.objects.normalize_email(email)
    except DjangoValidationError as e:
        raise ValidationError(e.message, e.code)
    with transaction.atomic():
        otp_session = MailOTPSession(email=email, data={"email": email})
        otp_session.save()
        otp_session.send("you want to change your email to this address. ")
        request.session[MAIL_OTP_BASE_SESSION_KEY+"change_email"] = otp_session.pk
    return Response({})

@api_view(['POST'])
@permission_classes([IsVerified])
def change_email_response_view(request):
    otp = str(request.data.get('token', ''))
    pk = request.session.get(MAIL_OTP_BASE_SESSION_KEY+"change_email", None)
    if pk is None:
        raise ParseError()
    query = MailOTPSession.objects.filter(pk=int(pk))
    if not query.exists():
        raise ParseError()
    otp_session = query[0]
    data, available_attempts = otp_session.verify(otp=otp)
    if data is None:
        return Response(
            {
                "available_attempts": available_attempts
            },
            status = status.HTTP_401_UNAUTHORIZED
        )
    request.user.email = data['email']
    request.user.save()
    request.session.pop(MAIL_OTP_BASE_SESSION_KEY+"change_email", None)
    request.session.pop(MAIL_OTP_BASE_SESSION_KEY+"change_mail_cooldown", None)
    return Response({})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([EMAILOTPRateThrottle])
def lost_totp_secret_view(request):
    if not request.user.totp_device.is_active:
        raise ParseError()
    
    if MAIL_OTP_BASE_SESSION_KEY+'lost_totp_cooldown' in request.session and datetime.datetime.fromtimestamp(request.session[MAIL_OTP_BASE_SESSION_KEY+'lost_totp_cooldown']) > datetime.datetime.now():
        raise Throttled()
    request.session[MAIL_OTP_BASE_SESSION_KEY+'lost_totp_cooldown'] = (datetime.datetime.now() + datetime.timedelta(minutes=2)).timestamp()
    request.session.save()

    with transaction.atomic():
        otp_session = MailOTPSession(email=request.user.email)
        otp_session.save()
        otp_session.send("you lost your totp secret.")
        request.session[MAIL_OTP_BASE_SESSION_KEY+"lost_totp"] = otp_session.pk
    return Response({})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def lost_totp_secret_response_view(request):
    if not request.user.totp_device.is_active:
        raise ParseError()

    otp = str(request.data.get('token', ''))
    pk = request.session.get(MAIL_OTP_BASE_SESSION_KEY+"lost_totp", None)
    if pk is None:
        raise ParseError()
    query = MailOTPSession.objects.filter(pk=int(pk))
    if not query.exists():
        raise ParseError()
    otp_session = query[0]
    data, available_attempts = otp_session.verify(otp=otp)
    if data is None:
        return Response(
            {
                "available_attempts": available_attempts
            },
            status = status.HTTP_401_UNAUTHORIZED
        )
    new_secret = pyotp.random_base32()
    request.user.totp_device.secret = new_secret
    request.user.totp_device.save()
    request.session.pop(MAIL_OTP_BASE_SESSION_KEY+"lost_totp", None)
    request.session.pop(MAIL_OTP_BASE_SESSION_KEY+'lost_totp_cooldown', None)
    return Response({
        "secret": new_secret,
        "auth_uri": pyotp.TOTP(new_secret).provisioning_uri(name=request.user.email, issuer_name="KISA")
    })

@api_view(['POST'])
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return Response({
        'is_authenticated': False,
        'data': None
    })

@api_view(['GET'])
def userinfo_view(request):
    data = dict()
    if request.user.is_authenticated: 
        for (_, db_identifier) in User.KSSO_KEYS_AND_FIELDS:
            data[db_identifier] = getattr(request.user, db_identifier, None)
    return Response({
        "is_authenticated": request.user.is_authenticated,
        "data": data
    })