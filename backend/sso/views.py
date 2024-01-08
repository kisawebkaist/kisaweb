import base64, json, os, secrets, urllib.parse

from django.http.response import HttpResponseRedirect
from web.settings import SECRET_KEY, ALLOWED_HOSTS

from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout
from django.shortcuts import render
from django.shortcuts import redirect

from sso.models import User, LoginError
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views import View
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

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
    if request.user and request.user.is_authenticated:
        return HttpResponseRedirect(ensure_relative_url(next))

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

def login_response_view(request):

    if bool(request.POST.get('success')):

        params = {
            'state': request.POST.get('state', ''),
            'raw_result': request.POST.get('result', ''),
            'http_host': request.META.get('HTTP_HOST', ''),
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
        return HttpResponseRedirect(ensure_relative_url(next))
    
    context = request.GET
    saved_state = request.session.get(KSSO_STATE_KEY)
    del request.session[KSSO_STATE_KEY]
    
    if saved_state is None or saved_state != context.get('state'):
        return redirect('login-error')
    
    #TODO: proper error handling and logging
    try:
        result = decrypt(context.get('raw_result'), context.get('state'), context.get('http_host') [:2]).decode('utf-8')
        result = json.loads(result, encoding='utf-8')

        user_info = result['dataMap']['USER_INFO']
            
        if not User.objects.filter(pk=user_info['kaist_uid']).exists():
            user_params = {}
            for key, field in keys_and_fields:
                if key in user_info:
                    user_params[field] = user_info.get(key)

            username = user_params['full_name']
            for c in "!#$%^&*(),./<>?\|":
                username = username.replace(c, '')
            username = username.strip()
            username = username.replace(' ', '_')
            user_params['username'] = f"{username}_{user_params['kaist_uid']}"
            user = User(**user_params)

            user.full_clean()
            
            user.save()
        else:
            user = User.objects.get(pk=user_info['kaist_uid'])

        login(request, user)
        return HttpResponseRedirect(ensure_relative_url(next))
    
    except Exception as e:
        return redirect('login-error')

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
