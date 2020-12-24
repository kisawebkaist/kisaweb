import os
import requests
import contextlib
from dotenv import load_dotenv
from xml.etree import ElementTree

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User

from .models import Agreement, LoginError

# Create your views here.

KSSO_REQUEST_LOGIN_URL = 'https://iam.kaist.ac.kr/iamps/requestLogin.do'
KSSO_SINGLE_AUTH_URL = 'https://iam.kaist.ac.kr/iamps/services/singlauth'

KSSO_SINGLE_AUTH_SOAP_REQUEST = '''
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="http://server.com">
        <soapenv:Header/>
        <soapenv:Body>
            <ser:verification>
                <cookieValue>{token}</cookieValue>
                <publicKeyStr>{publickey}</publicKeyStr>
                <adminVO>
                    <adminId></adminId>
                    <password></password>
                </adminVO>
            </ser:verification>
        </soapenv:Body>
    </soapenv:Envelope>'''

TEMP_USERDATA_SESSION_KEY = os.environ['TEMP_USERDATA_SESSION_KEY']
KSSO_PUBLIC_KEY = os.environ['KSSO_PUBLIC_KEY']


def login_view(request):
    return redirect(KSSO_REQUEST_LOGIN_URL)


def logout_view(request):
    logout(request)
    return redirect('/')


def login_error(request):
    return render(request, 'sso/login_error.html', context={
        'agreement': Agreement.objects.all()[0],
        'loginerror': LoginError.objects.all()[0],
    })


def agreement_show(request):
    user_data = request.session.get(TEMP_USERDATA_SESSION_KEY, None)
    agreement = Agreement.objects.all()[0]
    return render(request, 'sso/agreement.html', context={'user_data': user_data, 'agreement': agreement})


@require_http_methods(['POST'])
def agreement_process(request):
    agree_status = request.POST['agree']
    if agree_status == 'agree':
        user_data = request.session.get(TEMP_USERDATA_SESSION_KEY)
        if user_data is None:
            return redirect('/')
        user = User(
            username=user_data['kaist_uid'],
            first_name=user_data['givenname'],
            last_name=user_data['sn'],
            email=user_data['mail'] or ''
        )
        user.save()
        login(request, user)
    elif agree_status == 'disagree':
        with contextlib.suppress(KeyError):
            del request.session[TEMP_USERDATA_SESSION_KEY]

    return redirect('/')


def agreement(request):
    if request.method == "GET":
        return agreement_show(request)
    elif request.method == "POST":
        return agreement_process(request)


def validate_view(request):
    user_data = validate(request)

    if user_data is None:
        return redirect('login-error')
    else:
        try:
            user = User.objects.get(username=user_data['kaist_uid'])
            login(request, user)
            return redirect('/')
        except User.DoesNotExist:
            request.session[TEMP_USERDATA_SESSION_KEY] = user_data
            return redirect('sso-agreement')


def validate(request):
    token = request.COOKIES.get('SATHTOKEN')
    if not token:
        return None

    public_key = KSSO_PUBLIC_KEY
    soap_request_str = KSSO_SINGLE_AUTH_SOAP_REQUEST.format(token=token, public_key=public_key)
    try:
        soap_response = requests.post(KSSO_SINGLE_AUTH_URL, data=soap_request_str)
    except requests.exceptions.RequestException:
        return None

    # Parse SOAP response
    soap_xml = soap_response.text
    try:
        root = ElementTree.fromstring(soap_xml)
    except ElementTree.ParseError:
        return None

    keys = [
        'c', 'employeeType', 'kaist_uid', 'ku_acad_prog_eng', 'ku_born_date',
        'ku_campus', 'ku_ch_mail', 'ku_prog_start_date', 'ku_sex', 'ku_std_no',
        'givenname', 'sn', 'mail', 'ku_campus', 'mobile',
    ]
    user_data = {}
    for key in keys:
        tag = root.find('.//' + key)
        user_data[key] = None if tag is None else tag.text

    if user_data['kaist_uid'] is None:
        return None
    else:
        return user_data


def ksso_php(request):
    return redirect('validate-sso')
