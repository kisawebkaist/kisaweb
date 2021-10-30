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
import requests
import json
import datetime

from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout
from django.shortcuts import redirect

from sso.models import User
from django.views import View
from django.http import HttpResponse

# KSSO_LOGIN_URL = 'https://iam2dev.kaist.ac.kr/api/sso/commonLogin'
KSSO_LOGIN_URL = 'https://iam2dev.kaist.ac.kr/api/sso/commonLogin'
KSSO_LOGOUT_URL = 'https://iam2.kaist.ac.kr/api/api/sso/logout'
KSSO_CLIENT_ID = os.environ.get('KSSO_CLIENT_ID')


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import base64
import hashlib
from Crypto.Cipher import AES

def decrypt(data, state, host) :
    BS = AES.block_size 
    #pad=lambda s:s+(BS-len(s)%BS)*chr(BS-len(s)%BS) 
    # unpad = lambda s : s[0:-ord(s[-1])] 
    unpad = lambda s : s[0:-s[-1]] 
    if host in ('ka', 'co','ca') :
        key = (CAIS_AES_ID_SECRET+str(state))[80:96] # 32bit
    else :
        key = (SA_AES_ID_SECRET+str(state))[80:96] # 32bit
    iv=key[:16] # 16bit
    cipher = AES.new(key, AES.MODE_CBC, IV=iv) 
    deciphed = cipher.decrypt(base64.b64decode(data))   
    # print(deciphed[-1])
    deciphed = unpad(deciphed)
    return deciphed


@method_decorator(csrf_exempt, name='dispatch')
class SSOLoginRedirect(View):
    def get(self, request):
        state = str(int(time()))
        request.session['state'] = state

        data = {
            'client_id': "client_022",
            # 'redirect_url': reverse('login'),
            'redirect_url': 'http://localhost:8000/sso/login/',
            'state': state,
        }
        # response = requests.post(url=KSSO_LOGIN_URL, data=data)

        # django_response = HttpResponse(
        #     content         = response.content,
        #     status          = response.status_code,
        #     content_type    = response.headers['Content-Type']
        # )
        # print(django_response.content)
        redirect_url    = f'{KSSO_LOGIN_URL}?client_id={data["client_id"]}&state={data["state"]}&redirect_url={data["redirect_url"]}'
        print(redirect_url)
        return redirect(redirect_url)

    def post(self, request):
        if bool(request.POST.get('success')):
            # state validation
            state = request.POST.get('state')
            if request.session.get('state'):
                saved_state = request.session.get('state')
                if not saved_state == state:
                    # state validation failure handling
                    pass
                del request.session['state']

            # k_uid
            k_uid = request.POST.get('k_uid')
            # result object JSON string
            # result_str = request.POST.get('result')
            # result = json.loads(result_str, encoding='utf-8')
            print(request.META.get('HTTP_HOST'))
            decrypted_data = decrypt(k_uid, state, request.META.get('HTTP_HOST') [:2])
            request.session['kaist_uid'] = decrypted_data
            result = request.POST.get('result')
            print(result)
            print(base64.b64decode(result))
            result = decrypt(result, state, request.META.get('HTTP_HOST') [:2]).decode('utf-8')
            print(result)
            # User information
            user_info = result['dataMap']['USER_INFO']

            if not User.objects.filter(pk=user_info['kaist_uid']).exists():
                keys = [
                    'kaist_uid', 'ku_kname', 'displayname', 'sn', 'givenname',
                    'ku_born_date', 'c', 'ku_sex',
                    'mail', 'ku_ch_mail',
                    'ku_employee_number', 'ku_std_no', 'ku_acad_org', 'ku_acad_name', 'ku_campus',
                    'title', 'ku_psft_user_status', 'ku_psft_user_status_kor',
                    'ku_acad_prog_code', 'ku_acad_prog', 'ku_acad_prog_eng',
                    'employeeType', 'ku_prog_effdt', 'ku_stdnt_type_id', 'ku_stdnt_type_class', 'ku_category_id',
                    'ku_prog_start_date', 'ku_prog_end_date',
                    'acad_ebs_org_id', 'uid',
                    'acad_ebs_org_name_eng', 'acad_ebs_org_name_kor',
                ]
                user_params = {}
                for key in keys:
                    user_params[key] = user_info[key]
                user = User(**user_params)
                user.save()
            else:
                user = User.objects.get(pk=user_info['kaist_uid'])

            login(request, user)
            return redirect('/')
        else:
            # TODO: Make login failed message/page
            return redirect('/')

def sso_logout_redirect(request):
    data = {
        'client_id': KSSO_CLIENT_ID,
        'redirect_url': reverse_lazy('sso_logout_response'),
    }

    response = requests.post(url=KSSO_LOGOUT_URL, data=data)
    return response


def sso_logout_response(request):
    # django logout
    logout(request)
    return redirect('/')
