# import os
# import requests
# import contextlib
# from dotenv import load_dotenv
# from xml.etree import ElementTree

# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.contrib.auth import login, logout
# from django.views.decorators.http import require_http_methods
# from django.contrib.auth.models import User

# from .models import Agreement, LoginError

# Create your views here.

# KSSO_REQUEST_LOGIN_URL = 'https://iam.kaist.ac.kr/iamps/requestLogin.do'
# KSSO_SINGLE_AUTH_URL = 'https://iam.kaist.ac.kr/iamps/services/singlauth'

# KSSO_SINGLE_AUTH_SOAP_REQUEST = '''
#     <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="http://server.com">
#         <soapenv:Header/>
#         <soapenv:Body>
#             <ser:verification>
#                 <cookieValue>{token}</cookieValue>
#                 <publicKeyStr>{publickey}</publicKeyStr>
#                 <adminVO>
#                     <adminId></adminId>
#                     <password></password>
#                 </adminVO>
#             </ser:verification>
#         </soapenv:Body>
#     </soapenv:Envelope>'''

# TEMP_USERDATA_SESSION_KEY = os.environ['TEMP_USERDATA_SESSION_KEY']
# KSSO_PUBLIC_KEY = os.environ['KSSO_PUBLIC_KEY']


# def login_view(request):
#     return redirect(KSSO_REQUEST_LOGIN_URL)


# def logout_view(request):
#     logout(request)
#     return redirect('/')


# def login_error(request):
#     return render(request, 'sso/login_error.html', context={
#         'agreement': Agreement.objects.all()[0],
#         'loginerror': LoginError.objects.all()[0],
#     })


# def agreement_show(request):
#     user_data = request.session.get(TEMP_USERDATA_SESSION_KEY, None)
#     agreement = Agreement.objects.all()[0]
#     return render(request, 'sso/agreement.html', context={'user_data': user_data, 'agreement': agreement})


# @require_http_methods(['POST'])
# def agreement_process(request):
#     agree_status = request.POST['agree']
#     if agree_status == 'agree':
#         user_data = request.session.get(TEMP_USERDATA_SESSION_KEY)
#         if user_data is None:
#             return redirect('/')
#         user = User(
#             username=user_data['kaist_uid'],
#             first_name=user_data['givenname'],
#             last_name=user_data['sn'],
#             email=user_data['mail'] or ''
#         )
#         user.save()
#         login(request, user)
#     elif agree_status == 'disagree':
#         with contextlib.suppress(KeyError):
#             del request.session[TEMP_USERDATA_SESSION_KEY]

#     return redirect('/')


# def agreement(request):
#     if request.method == "GET":
#         return agreement_show(request)
#     elif request.method == "POST":
#         return agreement_process(request)


# def validate_view(request):
#     user_data = validate(request)

#     if user_data is None:
#         return redirect('login-error')
#     else:
#         try:
#             user = User.objects.get(username=user_data['kaist_uid'])
#             login(request, user)
#             return redirect('/')
#         except User.DoesNotExist:
#             request.session[TEMP_USERDATA_SESSION_KEY] = user_data
#             return redirect('sso-agreement')


# def validate(request):
#     token = request.COOKIES.get('SATHTOKEN')
#     if not token:
#         return None

#     public_key = KSSO_PUBLIC_KEY
#     soap_request_str = KSSO_SINGLE_AUTH_SOAP_REQUEST.format(token=token, public_key=public_key)
#     try:
#         soap_response = requests.post(KSSO_SINGLE_AUTH_URL, data=soap_request_str)
#     except requests.exceptions.RequestException:
#         return None

#     # Parse SOAP response
#     soap_xml = soap_response.text
#     try:
#         root = ElementTree.fromstring(soap_xml)
#     except ElementTree.ParseError:
#         return None

#     keys = [
#         'c', 'employeeType', 'kaist_uid', 'ku_acad_prog_eng', 'ku_born_date',
#         'ku_campus', 'ku_ch_mail', 'ku_prog_start_date', 'ku_sex', 'ku_std_no',
#         'givenname', 'sn', 'mail', 'ku_campus', 'mobile',
#     ]
#     user_data = {}
#     for key in keys:
#         tag = root.find('.//' + key)
#         user_data[key] = None if tag is None else tag.text

#     if user_data['kaist_uid'] is None:
#         return None
#     else:
#         return user_data


# def ksso_php(request):
#     return redirect('validate-sso')

import os
from time import time
from django.http.response import HttpResponseRedirect
import requests
import json
import datetime

from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout
from django.shortcuts import redirect

from sso.models import User
from django.views import View
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

KSSO_LOGIN_URL = os.environ.get('KSSO_LOGIN_URL')
KSSO_LOGOUT_URL = os.environ.get('KSSO_LOGOUT_URL')

KSSO_CLIENT_ID = os.environ.get('KSSO_CLIENT_ID')
CAIS_AES_ID_SECRET = os.environ.get('KSSO_SECRET_KEY')
SA_AES_ID_SECRET = os.environ.get('KSSO_SECRET_KEY')


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import base64
import hashlib
from Crypto.Cipher import AES

def decrypt(data, state, host) :
    BS = AES.block_size 
    unpad = lambda s : s[0:-s[-1]] 
    if host in ('ka', 'co','ca') :
        key = (CAIS_AES_ID_SECRET+str(state))[80:96] # 32bit
    else :
        key = (SA_AES_ID_SECRET+str(state))[80:96] # 32bit
    iv=key[:16] # 16bit
    cipher = AES.new(key, AES.MODE_CBC, IV=iv) 
    deciphed = cipher.decrypt(base64.b64decode(data))   
    deciphed = unpad(deciphed)
    return deciphed

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

# TODO: Make agreement views

def login_view(request):
    state = str(int(time()))

    # TODO: Decide what to valide in state. Namely, what should state keep

    data = {
        'client_id': KSSO_CLIENT_ID,
        'redirect_url': request.build_absolute_uri(reverse('login-response')),
        'state': state,
    }

    redirect_url = f"{KSSO_LOGIN_URL}?{'&'.join([f'{key}={value}' for key, value in data.items()])}"
    return redirect(redirect_url)

@require_http_methods(['POST'])
@csrf_exempt
def login_response_view(request):
    if bool(request.POST.get('success')):
        # state validation
        state = request.POST.get('state')
        if request.session.get('state'):
            saved_state = request.session.get('state')
            if not saved_state == state:
                # state validation failure handling
                # TODO: Decide what to valide in state
                pass
            del request.session['state']

        result = request.POST.get('result')
        result = decrypt(result, state, request.META.get('HTTP_HOST') [:2]).decode('utf-8')
        result = json.loads(result, encoding='utf-8')
        
        # User information
        user_info = result['dataMap']['USER_INFO']

        if not User.objects.filter(pk=user_info['kaist_uid']).exists():
            
            user_params = {}
            for key, field in keys_and_fields:
                if key in user_info:
                    user_params[field] = user_info[key]
            user = User(**user_params)
            user.save()
        else:
            user = User.objects.get(pk=user_info['kaist_uid'])

        login(request, user)
        return redirect('/')
    else:
        # TODO: Make login failed message/page
        return redirect('/')

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
