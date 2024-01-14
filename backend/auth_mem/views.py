from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import JsonResponse
from django.utils.translation import gettext as _

from rest_framework.decorators import api_view, throttle_classes
from rest_framework.exceptions import ParseError, PermissionDenied, ValidationError
import rest_framework.status as status

from core.throttling import ScopedRateThrottle
from core.exceptions import IncorrectEndpointException
from sso.decorators import klogin_required

from .models import User, SignupToken

class UsernameCheckRateThrottle(ScopedRateThrottle):
    scope_attr = 'usernamecheck'

@api_view(['POST'])
def login_view(request):
    if request.kaist_profile.is_authenticated:
        if not User.objects.exists(kaist_profile=request.kaist_profile.pk):
            return JsonResponse(
                {
                    'detail': _('No such member exists with current kaist login credentials.')
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        username = User.objects.get(kaist_profile=request.kaist_profile.pk).username
    elif not "username" in request.data:
        raise ParseError(detail=_('Username was not provided.'))
    else:
        username = request.data["username"]
    
    if not "password" in request.data:
        raise ParseError(detail=_('Password was not provided.'))
    
    password = request.data["password"]
    user = authenticate(username, password)
    if user is None:
       raise PermissionDenied(detail=_('Incorrect login credentials provided.'))
    
    login(request, user)
    return JsonResponse(
        data=None
    )

@api_view(['POST'])
def logout_view(request):
    if request.kaist_profile.is_authenticated and not request.user.is_authenticated:
        return IncorrectEndpointException(detail=_("Use the other endpoint to logout."))
    logout(request)
    # TODO: to find out 
    # (1) if it is neccessary to log out of kaist sso
    return JsonResponse(
        data=None
    )

# TODO: Implement email verification, password change
@api_view(['GET'])
@throttle_classes([UsernameCheckRateThrottle])
@klogin_required
def check_username_exists(request):
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
        data=None
    )
    
