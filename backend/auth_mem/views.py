import urllib.parse

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import EmailValidator
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings
from django.utils.translation import gettext as _

from rest_framework.decorators import api_view, throttle_classes
from rest_framework.exceptions import ParseError, PermissionDenied, ValidationError
import rest_framework.status as status

from core.throttling import ScopedRateThrottle
from core.exceptions import IncorrectEndpointException
from sso.decorators import klogin_required

from .models import User, SignupToken
from .decorators import login_required
from .utils import MailVerificationCode
from core.utils import ensure_relative_url
from sso.views import KSSO_LOGOUT_URL, KSSO_CLIENT_ID

class UsernameCheckRateThrottle(ScopedRateThrottle):
    scope_attr = 'usernamecheck'

class MailVerificationCodeRateThrottle(ScopedRateThrottle):
    scope_attr = 'verification'

email_validator = EmailValidator()

@api_view(['POST'])
def login_view(request):
    """
    Format
    ------
    {
        'username': <username optional if klogined>,
        'password': <password>
        'next': <the url to be redirected after login>
    }

    For Frontend
    ------------
    - Make post request and follow the redirect
    """
    next = ensure_relative_url(request.data.get('next', '/'))
    redirect_klogout = request.kaist_profile.is_authenticated

    if request.kaist_profile.is_authenticated:
        query = User.objects.filter(kaist_profile=request.kaist_profile.pk)
        if not query.exists():
            return JsonResponse(
                {
                    'detail': _('No such member exists with current kaist login credentials.')
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        username = query[0].username
    elif not "username" in request.data:
        raise ParseError(detail=_('Username was not provided.'))
    else:
        username = request.data["username"]
    
    if not "password" in request.data:
        raise ParseError(detail=_('Password was not provided.'))
    
    password = request.data["password"]
    user = authenticate(username=username, password=password)
    if user is None:
       raise PermissionDenied(detail=_('Incorrect login credentials provided.'))
    
    login(request, user)
    
    if redirect_klogout:
        # need to logout from ksso
        data = {
            'client_id': KSSO_CLIENT_ID,
            'redirect_url': request.build_absolute_uri(next)
        }
        return HttpResponseRedirect(f"{KSSO_LOGOUT_URL}?{urllib.parse.urlencode(data)}")
    
    return HttpResponseRedirect(next)

@api_view(['POST'])
def logout_view(request):
    """
    For Frontend
    ------------
    - Make a post request and follow the redirect
    """
    if request.kaist_profile.is_authenticated and not request.user.is_authenticated:
        return IncorrectEndpointException(detail=_("Use the other endpoint to logout."))
    logout(request)
    return HttpResponseRedirect('/')

@api_view(['GET'])
@throttle_classes([UsernameCheckRateThrottle])
@klogin_required
def check_username_view(request):
    if not SignupToken.exists(request.kaist_profile):
        raise PermissionDenied()
    
    username = request.GET.get('username')
    if username is None or username == '':
        raise ParseError(detail=_('No username provided.'))
    
    return JsonResponse(
        {'exists': User.objects.exists(username=username)}
    )
    

@api_view(['POST'])
@klogin_required
def signup_view(request):
    """
    Format
    ------
    {
        'username': <username>,
        'password': <password>,
    }
    """
    token = SignupToken.get(request.kaist_profile)
    if token is None:
        raise PermissionDenied()
    username = request.data.get('username', '')
    password = request.data.get('password', '')
    
    if User.objects.exists(username=username):
        raise ParseError()
    
    try:
        User.username.run_validators(username)
        validate_password(password)
    except DjangoValidationError as e:
        raise ValidationError(detail=e.error_dict, code=e.code)
    
    token.use(username, password)

    return JsonResponse(
        data={}
    )
    
@api_view(['POST'])
@throttle_classes([MailVerificationCodeRateThrottle])
@login_required
def register_mail_view(request):
    """
    Format
    ------
    {
        'email': <email to be registered>
    }
    """
    email = request.data.get('email', '')
    try:
        email_validator(email)
        email = User.objects.normalize_email(email)
    except DjangoValidationError as e:
        raise ValidationError(e.error_dict, e.code)
    
    code_obj = MailVerificationCode.new(email)
    code_obj.saveForMailRegistraion(request.session, request.user.username)
    return JsonResponse(
        data={}
    )

@api_view(['POST'])
@login_required
def attempt_mail_reg_view(request):
    """
    Format
    ------
    {
        'code' : <verification code>
    }
    """
    code = request.data.get('code', '')
    email, num_avai_attempts = MailVerificationCode.attempt_reg(request.session, code)
    if email is None:
        raise JsonResponse(
            {'num_avai_attempts': num_avai_attempts},
            status = status.HTTP_403_FORBIDDEN
        )
    request.user.email = email
    request.user.save()
    return JsonResponse(
        data={}
    )

@api_view(['POST'])
@throttle_classes([MailVerificationCodeRateThrottle])
@klogin_required
def change_pw_view(request):
    """
    Format
    ------
    {
        'password': <new password>
    }
    """
    query = User.objects.filter(kaist_profile=request.kaist_profile.pk)
    if not query.exists():
        raise PermissionDenied()

    user = query[0]
    if (not user.email) or user.email == '':
        raise ValidationError(detail=_(f'Sorry, you don\'t have registered mail. Please contact {settings.DEVELOPER_MAIL}.'))
    
    password = request.data.get('password', '')
    try:
        validate_password(password)
    except DjangoValidationError as e:
        raise ValidationError(e.error_dict, e.code)
    
    code_obj = MailVerificationCode.new(user.email)
    code_obj.saveForPasswordChange(request.session, password)
    return JsonResponse(
        data={}
    )

@api_view(['POST'])
@klogin_required
def attempt_pw_change_view(request):
    """
    Format
    ------
    {
        'code': <verification code>
    }
    """
    query = User.objects.filter(kaist_profile=request.kaist_profile.pk)
    if not query.exists():
        raise PermissionDenied()
    
    user = query[0]
    code = request.data.get('code', '')
    password, num_avai_attempts = MailVerificationCode.attempt_pw(request.session, code)
    if password is None:
        raise JsonResponse(
            {'num_avai_attempts': num_avai_attempts},
            status = status.HTTP_403_FORBIDDEN
        )
    user.set_password(password)
    user.save()
    update_session_auth_hash(request, user)
    return JsonResponse(
        data = {}
    )