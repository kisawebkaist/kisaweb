import base64, json, logging, urllib.parse, pyotp

from corsheaders.signals import check_request_enabled

from django.conf import settings
from django.contrib.auth import login, logout
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext as _

from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from rest_framework.exceptions import PermissionDenied, ParseError, ValidationError
from rest_framework.parsers import FormParser
from rest_framework.response import Response
import rest_framework.status as status

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from . import TOTP_SESSION_KEY
from .models import User, MailOTPSession
from .permissions import IsKISA, IsKISAVerified
from core.utils import ensure_relative_url, get_random_urlsafe_string, CSRFExemptSessionAuthentication

KSSO_LOGIN_URL = settings.KSSO_LOGIN_URL
KSSO_LOGOUT_URL = settings.KSSO_LOGOUT_URL
KSSO_CLIENT_ID = settings.KSSO_CLIENT_ID
KSSO_ORIGIN = settings.KSSO_ORIGIN
KSSO_SA_AES_ID_SECRET = settings.KSSO_SA_AES_ID_SECRET
MAIL_OTP_BASE_SESSION_KEY = "_mail_otp_" 

logger = logging.getLogger(__name__)
email_validator = EmailValidator()

#TODO: throttle any request that triggers "send-mail"

def decrypt(data, state):
    try:
        BS = AES.block_size 
        key = (KSSO_SA_AES_ID_SECRET+str(state))[80:96].encode("utf8") # 128 bit
        cipher = AES.new(key, AES.MODE_CBC, IV=key)
        deciphed = cipher.decrypt(base64.b64decode(data))   
        deciphed = unpad(deciphed, BS).decode('utf-8')
        return deciphed
    except ValueError as e:
        logger.warning("Suspicious operation: decryption failed: %s", e)
        raise ParseError()


@api_view(['POST'])
def login_view(request):
    next = ensure_relative_url(str(request.data.get('next', '/')))

    if request.user.is_authenticated:
        return HttpResponseRedirect(next)

    if request.session.get('state') is None:
        state = get_random_urlsafe_string(8)
        request.session['state'] = state
        request.session['next'] = next
    else:
        state = request.session['state']

    data = {
        'client_id': KSSO_CLIENT_ID,
        'redirect_url': request.build_absolute_uri(reverse('login-response')),
        'state': state,
    }
    return HttpResponseRedirect(f"{KSSO_LOGIN_URL}?{urllib.parse.urlencode(data)}")


def cors_allow_login_response(sender, request, **kwargs):
    """
    In login_response view, a cross-site POST request is sent from SSO website. This allows CORS for that.
    """
    return True
    # return request.resolver_match.url_name == 'login-response' and request.headers.get("origin", None) == KSSO_ORIGIN

check_request_enabled.connect(cors_allow_login_response)

@api_view(['POST'])
@parser_classes([FormParser])
@authentication_classes([CSRFExemptSessionAuthentication])
def login_response_view(request):
    """
    This POST request is supposed to be sent by SSO website and contains encrypted user information.
    This view is csrf_exempted but we will enforce strict origin-checking manually.
    We also need to allow CORS from sso website with credentials.
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    
    state = str(request.data.get('state', '00000000'))
    raw_result = str(request.data.get('result', ''))
    success = request.data.get('success')
    origin = request.META.get('HTTP_ORIGIN')
    saved_state = request.session.pop('state', '')
    next = request.session.pop('next', '/')

    if not bool(success) or raw_result == "" or saved_state == "" or not isinstance(state, str) or saved_state != state:
        raise ParseError()

    if not origin == KSSO_ORIGIN:
        logger.info(f"Suspicious Operation: Invalid origin in login-response: (user-agent: {request.META.get('HTTP_USER_AGENT')}, origin: {origin})")
        raise PermissionDenied(detail=_(f'CSRF Failed: Origin checking failed - {origin} does not match any trusted origins.'))

    result = decrypt(raw_result, state)
    
    try:
        result = json.loads(result)
        user = User.from_info_json(result['dataMap']['USER_INFO'])
        login(request, user)
        request.session.pop(TOTP_SESSION_KEY, None)
        # the errors in here might indicate just simple data corruption or secret-key leak
    except KeyError as e:
        logger.warning(f'Suspicious Operation: key error: %s', e)
        raise ParseError()
    except json.JSONDecodeError as e:
        logger.warning(f'Suspicious Operation: json decoding failed: %s', e)
        raise ParseError()
    except DjangoValidationError as e:
        logger.warning(f'Suspicious Operation: user model validation failed: %s', e)
        raise ParseError()
    
    return HttpResponseRedirect(next)

@api_view(['POST'])
@permission_classes([IsKISA])
def check_totp_view(request):
    if request.user.totp_device.verify(str(request.data.get('token', ''))):
        request.session.cycle_key()
        request.session[TOTP_SESSION_KEY] = True
    else: 
        raise ParseError()
    return Response({})

@api_view(['POST'])
@permission_classes([IsKISAVerified])
def change_totp_secret(request):
    new_secret = pyotp.random_base32()
    request.user.totp_device.secret = new_secret
    request.user.totp_device.save()
    return Response({
        "secret": new_secret,
        "auth_uri": pyotp.TOTP(new_secret).provisioning_uri(name=request.user.email, issuer_name="KISA")
    })


@api_view(['POST'])
@permission_classes([IsKISAVerified])
def change_email_view(request):
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
@permission_classes([IsKISAVerified])
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
    return Response({})


@api_view(['POST'])
@permission_classes([IsKISA])
def lost_totp_secret_view(request):
    with transaction.atomic():
        otp_session = MailOTPSession(email=request.user.email)
        otp_session.save()
        otp_session.send("you lost your totp secret.")
        request.session[MAIL_OTP_BASE_SESSION_KEY+"lost_totp"] = otp_session.pk
    return Response({})

@api_view(['POST'])
@permission_classes([IsKISA])
def lost_totp_secret_response_view(request):
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
    return Response({
        "secret": new_secret,
        "auth_uri": pyotp.TOTP(new_secret).provisioning_uri(name=request.user.email, issuer_name="KISA")
    })

@api_view(['POST'])
def logout_view(request):
    next = ensure_relative_url(str(request.data.get('next', '/')))
    if not request.user.is_authenticated:
        return HttpResponseRedirect(next)
    
    logout(request)
    
    data = {
        'client_id': KSSO_CLIENT_ID,
        'redirect_url': request.build_absolute_uri(next),
    }

    return HttpResponseRedirect(f"{KSSO_LOGOUT_URL}?{urllib.parse.urlencode(data)}")