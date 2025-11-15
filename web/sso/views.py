import os
from time import time
from django.core.exceptions import SuspiciousOperation, ValidationError
from django.http.response import HttpResponseRedirect
import requests
import json
import datetime
from web.settings import SECRET_KEY

import urllib.parse

from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout
from django.shortcuts import render
from django.shortcuts import redirect

from sso.models import User, LoginError
from django.views import View
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt

import base64
from Crypto.Cipher import AES

import secrets
import hashlib

KSSO_LOGIN_URL = os.environ.get('KSSO_LOGIN_URL')
KSSO_LOGOUT_URL = os.environ.get('KSSO_LOGOUT_URL')

KSSO_CLIENT_ID = os.environ.get('KSSO_CLIENT_ID')
KSSO_STATE_KEY = os.environ.get('KSSO_STATE_KEY')

CAIS_AES_ID_SECRET = os.environ.get('KSSO_SECRET_KEY')
SA_AES_ID_SECRET = os.environ.get('KSSO_SECRET_KEY')

keys_and_fields = [
    ('kaist_uid', 'kaist_uid'), 
    ('ku_kname', 'korean_name'), 
    ('displayname', 'full_name'), 
    ('sn', 'first_name'), 
    ('givenname', 'last_name'),
    ('ku_born_date', 'dob'), 
    ('c', 'nationality'), 
    ('ku_sex', 'sex'),
    ('mail', 'kaist_email'), 
    ('ku_ch_mail', 'external_email'),
    ('ku_employee_number', 'employee_number'), 
    ('ku_std_no', 'student_number'), 
    ('ku_acad_org', 'bachelors_department_code'), 
    ('ku_acad_name', 'bachelors_department_name'), 
    ('ku_campus', 'campus'),
    ('title', 'title_english'), 
    ('ku_psft_user_status', 'student_status_english'), 
    ('ku_psft_user_status_kor', 'student_status_korean'),
    ('ku_acad_prog_code', 'degree_code'), 
    ('ku_acad_prog', 'degree_name_korean'), 
    ('ku_acad_prog_eng', 'degree_name_english'),
    ('employeeType', 'user_group'), 
    ('ku_prog_effdt', 'student_admission_datetime'), 
    ('ku_stdnt_type_id', 'student_type_id'), 
    ('ku_stdnt_type_class', 'student_type_class'), 
    ('ku_category_id', 'student_category_id'),
    ('ku_prog_start_date', 'student_enrollment_date'), 
    ('ku_prog_end_date', 'student_graduation_date'),
    ('acad_ebs_org_id', 'student_department_id'), 
    ('uid', 'sso_id'),
    ('acad_ebs_org_name_eng', 'student_department_name_english'), 
    ('acad_ebs_org_name_kor', 'student_department_name_korean'),
]

def ensure_relative_url(url):
    if url[0] == '/':
        return url
    url = urllib.parse.urlparse(url)._replace(scheme='', netloc='').geturl()
    if url == "" or url[0] != '/':
        url = '/' + url
    return url

def decrypt(data, state, host) :
    BS = AES.block_size 
    unpad = lambda s : s[0:-s[-1]] 
    if host in ('ka', 'co','ca') :
        key = (CAIS_AES_ID_SECRET+str(state))[80:96] # 32bit
    else :
        key = (SA_AES_ID_SECRET+str(state))[80:96] # 32bit
    iv=key[:16] # 16bit
    cipher = AES.new(key.encode("utf8"), AES.MODE_CBC, IV=iv.encode("utf8"))
    deciphed = cipher.decrypt(base64.b64decode(data))   
    deciphed = unpad(deciphed)
    return deciphed

def login_view(request):

    next = request.GET.get('next', '/')
    if request.user and request.user.is_authenticated:
        return redirect(next)

    if request.session.get(KSSO_STATE_KEY) is None:
        state = secrets.token_hex(16)
        request.session[KSSO_STATE_KEY] = state
    else:
        state = request.session[KSSO_STATE_KEY]

    data = {
        'client_id': KSSO_CLIENT_ID,
        'redirect_url': request.build_absolute_uri(reverse('login-response')) + '?next=' + next,
        'state': state,
    }

    redirect_url = f"{KSSO_LOGIN_URL}?{'&'.join([f'{key}={value}' for key, value in data.items()])}"
    return redirect(redirect_url)

@require_http_methods(['POST'])
@csrf_exempt
def login_response_view(request):

    origin = request.META.get('HTTP_ORIGIN')
    if origin != "https://iam2.kaist.ac.kr":
        useragent = request.META.get('HTTP_USER_AGENT')
        raise SuspiciousOperation(_(f'CSRF Failed: Origin checking failed - {origin} does not match any trusted origins. Sent by {useragent}'))

    if bool(request.POST.get('success')):

        params = {
            'state': request.POST.get('state'),
            'raw_result': request.POST.get('result'),
            'http_host': request.META.get('HTTP_HOST'),
            'next': request.GET.get('next', '/')
        }
        
        response = redirect('login-handler')
        response['Location'] = f'{response["Location"]}?{"&".join([f"{key}={urllib.parse.quote(value)}" for key, value in params.items()])}' 
        
        return response
    
    else:
        return redirect('login-error')

def login_handler_view(request):

    next = request.GET.get('next', '/')
    if request.user and request.user.is_authenticated:
        return redirect(next)

    context = request.GET
    saved_state = request.session.get(KSSO_STATE_KEY)
    del request.session[KSSO_STATE_KEY]
    
    if saved_state is None or saved_state != context.get('state'):
        return redirect('login-error')
    
    result = decrypt(context.get('raw_result'), context.get('state'), context.get('http_host') [:2]).decode('utf-8')

    try:
        result = json.loads(result)
        user = User.from_info_json(result['dataMap']['USER_INFO'])
        login(request, user)
    except KeyError as e:
        raise SuspiciousOperation(f'Key error {e} using {result}.')
    except json.JSONDecodeError as e:
        raise SuspiciousOperation(f'JSON decoding failed {e} using {result}')
    except ValidationError as e:
        raise SuspiciousOperation(f'User model validation failed {e} using {result}')
    
    return redirect(ensure_relative_url(next))

def login_error_view(request):
    return render(request, 'sso/login_error.html', {})

def logout_view(request):
    data = {
        'client_id': KSSO_CLIENT_ID,
        'redirect_url': request.build_absolute_uri(reverse('logout-response')),
    }
    location = f"{KSSO_LOGOUT_URL}?{'&'.join([f'{key}={value}' for key, value in data.items()])}"
    response = HttpResponseRedirect(location)
    return response

def logout_response_view(request):
    logout(request)
    return redirect('/')


# ============================================================================
# Pass-Ni SSO Integration (OAuth 2.0 style flow)
# ============================================================================

from django.conf import settings
from django.utils.crypto import constant_time_compare

# Pass-Ni configuration from settings
PASSNI_AUTH_URL = getattr(settings, 'PASSNI_AUTH_URL', None)
PASSNI_TOKEN_URL = getattr(settings, 'PASSNI_TOKEN_URL', None)
PASSNI_CLIENT_ID = getattr(settings, 'PASSNI_CLIENT_ID', None)
PASSNI_CLIENT_SECRET = getattr(settings, 'PASSNI_CLIENT_SECRET', None)
PASSNI_STATE_SESSION_KEY = getattr(settings, 'PASSNI_STATE_SESSION_KEY', 'passni_state')
PASSNI_NONCE_SESSION_KEY = getattr(settings, 'PASSNI_NONCE_SESSION_KEY', 'passni_nonce')
PASSNI_ENABLED = getattr(settings, 'PASSNI_ENABLED', False)


def passni_login_init_view(request):
    if not PASSNI_ENABLED:
        return redirect('login')
    
    next_url = request.GET.get('next', '/')
    
    # If already authenticated, just redirect
    if request.user and request.user.is_authenticated:
        return redirect(next_url)
    
    # Generate state and nonce for security
    state = secrets.token_hex(16)
    nonce = secrets.token_hex(16)
    
    # Store in session
    request.session[PASSNI_STATE_SESSION_KEY] = state
    request.session[PASSNI_NONCE_SESSION_KEY] = nonce
    
    # Build redirect URI to our callback
    redirect_uri = request.build_absolute_uri(reverse('passni-callback'))
    
    # Build authorization parameters
    auth_params = {
        'client_id': PASSNI_CLIENT_ID,
        'redirect_uri': redirect_uri,
        'state': state,
        'nonce': nonce,
    }
    
    # Render a page with auto-submit form (like the JSP example)
    context = {
        'auth_url': PASSNI_AUTH_URL,
        'auth_params': auth_params,
        'next': next_url,
    }
    
    return render(request, 'sso/passni_login_init.html', context)


@require_http_methods(['GET', 'POST'])
def passni_callback_view(request):
    if not PASSNI_ENABLED:
        return redirect('login-error')
    
    # Get code and state from request (could be GET or POST depending on provider)
    code = request.POST.get('code') or request.GET.get('code')
    req_state = request.POST.get('state') or request.GET.get('state')
    next_url = request.GET.get('next', '/')
    
    # Retrieve and clear state/nonce from session
    saved_state = request.session.pop(PASSNI_STATE_SESSION_KEY, None)
    saved_nonce = request.session.pop(PASSNI_NONCE_SESSION_KEY, None)
    
    # Validate state (CSRF protection)
    if saved_state is None or not constant_time_compare(saved_state, req_state or ''):
        raise SuspiciousOperation(_('Pass-Ni state validation failed - possible CSRF attack'))
    
    # Validate we got a code
    if not code:
        raise SuspiciousOperation(_('Pass-Ni did not return authorization code'))
    
    # Exchange authorization code for user info
    try:
        payload = {
            'client_id': PASSNI_CLIENT_ID,
            'client_secret': PASSNI_CLIENT_SECRET,
            'code': code,
            'redirect_uri': request.build_absolute_uri(reverse('passni-callback')),
        }
        
        response = requests.post(PASSNI_TOKEN_URL, data=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        
    except requests.exceptions.RequestException as e:
        raise SuspiciousOperation(f'Pass-Ni token exchange failed: {e}')
    except json.JSONDecodeError as e:
        raise SuspiciousOperation(f'Pass-Ni response is not valid JSON: {e}')
    
    # Check for error in response
    if 'errorCode' in data and data['errorCode']:
        raise SuspiciousOperation(f'Pass-Ni returned error: {data.get("errorCode")} - {data.get("errorMessage", "Unknown error")}')
    
    # Validate nonce (replay attack prevention)
    returned_nonce = data.get('nonce')
    if saved_nonce is None or not constant_time_compare(saved_nonce, returned_nonce or ''):
        raise SuspiciousOperation(_('Pass-Ni nonce validation failed - possible replay attack'))
    
    # Extract user info
    user_info = data.get('userInfo')
    if not user_info:
        raise SuspiciousOperation(_('Pass-Ni response missing userInfo'))
    
    # Transform Pass-Ni format to KAIST SSO format (if needed)
    # The User.from_info_json expects certain field names
    transformed_user_info = transform_passni_user_info(user_info)
    
    # Create or update user
    try:
        user = User.from_info_json(transformed_user_info)
        login(request, user)
    except (KeyError, ValidationError) as e:
        raise SuspiciousOperation(f'Failed to create/login user from Pass-Ni info: {e}')
    
    return redirect(ensure_relative_url(next_url))


def transform_passni_user_info(passni_info):
    # Based on JSP example and KAIST SSO field mapping
    # You may need to adjust these mappings based on actual Pass-Ni response
    
    transformed = {}
    
    # Direct mappings (if field names match)
    direct_fields = ['kaist_uid', 'uid', 'displayname', 'mail', 'employeeType']
    for field in direct_fields:
        if field in passni_info:
            transformed[field] = passni_info[field]
    
    # Field name mappings (Pass-Ni name -> KAIST SSO name)
    field_mappings = {
        'ku_kname': 'ku_kname',  # Korean name
        'sn': 'sn',  # surname
        'givenname': 'givenname',  # given name
        'ku_born_date': 'ku_born_date',
        'c': 'c',  # nationality
        'ku_sex': 'ku_sex',
        'ku_ch_mail': 'ku_ch_mail',  # external email
        'ku_employee_number': 'ku_employee_number',
        'ku_std_no': 'ku_std_no',  # student number
        'ku_acad_org': 'ku_acad_org',
        'ku_acad_name': 'ku_acad_name',
        'ku_campus': 'ku_campus',
        'title': 'title',
        'ku_psft_user_status': 'ku_psft_user_status',
        'ku_psft_user_status_kor': 'ku_psft_user_status_kor',
        'ku_acad_prog_code': 'ku_acad_prog_code',
        'ku_acad_prog': 'ku_acad_prog',
        'ku_acad_prog_eng': 'ku_acad_prog_eng',
        'ku_prog_effdt': 'ku_prog_effdt',
        'ku_stdnt_type_id': 'ku_stdnt_type_id',
        'ku_stdnt_type_class': 'ku_stdnt_type_class',
        'ku_category_id': 'ku_category_id',
        'ku_prog_start_date': 'ku_prog_start_date',
        'ku_prog_end_date': 'ku_prog_end_date',
        'acad_ebs_org_id': 'acad_ebs_org_id',
        'acad_ebs_org_name_eng': 'acad_ebs_org_name_eng',
        'acad_ebs_org_name_kor': 'acad_ebs_org_name_kor',
    }
    
    for passni_field, kaist_field in field_mappings.items():
        if passni_field in passni_info:
            transformed[kaist_field] = passni_info[passni_field]
    
    return transformed
