import json, base64, threading, requests
from urllib.parse import urlencode
from urllib.parse import parse_qs, urlparse

from django.conf import settings
from django.urls import reverse

from rest_framework.test import APIClient, APITestCase, APILiveServerTestCase
import rest_framework.status as status

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from .views import KSSO_SA_AES_ID_SECRET
from .models import *


def generate_user_info(
    kaist_uid: int = 1, 
    country: str = 'KR',
    kaist_email: str = 'nupjuk@kaist.ac.kr',
):
    return {
        'kaist_uid': kaist_uid,
        'ku_kname': 'NUPJUK KIM',
        'displayname': 'NUPJUK, KIM',
        'sn': 'KIM',
        'givenname': 'NUPJUK',
        'ku_born_date': '2024-01-01',
        'c': country,
        'ku_sex': 'M',
        'mail': kaist_email,
        'ku_ch_mail': 'nupjuk@gmail.com',
        'ku_std_no': '20240101',
        'ku_campus': 'D1/D1',
        'ku_psft_user_status': 'Enrollment',
        'ku_psft_user_status_kor': '재학',
        'ku_acad_prog_code': '0',
        'ku_acad_prog': '학사',
        'ku_acad_prog_eng': 'bachelor',
        'employeeType': 'S',
        'ku_stdnt_type_id': '18',
        'ku_stdnt_type_class': 'AID',
        'ku_category_id': 'F',
        'ku_prog_start_date': '2024-01-01',
        'uid': 'kimnupjuk',
        'ku_acad_org': '11872',
        'ku_acad_name': 'School of Computing',
        'title': 'Student',
        'acad_ebs_org_id': '9945',
        'acad_ebs_org_name_eng': 'School of Computing',
        'acad_ebs_org_name_kor': '전산학부'
    }

def encrypt(user_info: dict, state: str)->str:
    result_json = {
        'dataMap': {
            'USER_INFO': user_info
        }
    }
    result_padded = pad(json.dumps(result_json).encode(), 16)

    iv = (KSSO_SA_AES_ID_SECRET+state)[80:96].encode()
    cipher = AES.new(iv, AES.MODE_CBC, iv)

    return base64.b64encode(cipher.encrypt(result_padded)).decode()

def generate_user(
        kaist_uid = 1,
        country = 'KOR',
        kaist_email = 'nupjuk@kaist.ac.kr',
        kisa_division = 0,
        totp_secret = None
):
    user_json = generate_user_info(kaist_uid, country, kaist_email)
    user = User.from_info_json(user_json)
    user.kisa_division = kisa_division
    if totp_secret is not None:
        user.totp_device = TOTPDevice(secret=totp_secret)
        user.totp_device.save()
    return (user, user_json)

def get_cookie_value(jar, key, default=''):
    token = jar.get(key)
    if token is None:
        token = default
    else:
        token = token.value
    return token

def login(user:User, base_url="http://localhost:8080"):
    """a helper method to login to admin site in browser"""
    s = requests.session()
    s.get(base_url+reverse('state'))
    csrftoken = s.cookies['csrftoken']

    r = s.post(base_url+reverse('login'), headers={'X-CSRFToken': csrftoken}, allow_redirects=False)
    state = parse_qs(urlparse(r.headers['Location']).query)['state'][0]

    payload = {
        'result': encrypt(user.get_info_json(), state),
        'state': state,
        'success': 'true'
    }
    r = s.post(
        base_url+reverse('login-response'), 
        payload, 
        headers={
            'X-CSRFToken': csrftoken,
            'Origin': settings.KSSO_ORIGIN
        },
        allow_redirects=False
    )
    print(s.cookies)
    


class AuthTest(APITestCase):
    otp_mail = None
    def setUp(self):
        self.totp = pyotp.TOTP(pyotp.random_base32())
        self.test_user, self.test_user_json = generate_user(totp_secret=self.totp.secret, kisa_division=1)
        self.test_user.save()

    @classmethod
    def get_otp_mail(cls):
        if cls.otp_mail is None:
            cls.otp_mail = input("Type a email to receive otp codes: ")
        return cls.otp_mail

    def test_normal_login(self, client=APIClient(), user_info=generate_user_info(kaist_uid=2)):
        csrftoken = get_cookie_value(client.cookies, 'csrftoken')
        r = client.post(
            reverse('login'),
            {'next': '/'},
            headers = {'X-CSRFToken': csrftoken}
            )
        self.assertEqual(r.status_code, status.HTTP_302_FOUND)
        state = parse_qs(urlparse(r.headers['Location']).query)['state'][0]

        # login-reponse POST request from iam2
        payload = {
            'result': encrypt(user_info, state),
            'state': state,
            'success': 'true'
        }
        r = client.post(
            reverse('login-response'),
            urlencode(payload),
            headers = {'Origin': settings.KSSO_ORIGIN, 'X-CSRFToken': csrftoken},
            content_type='application/x-www-form-urlencoded'
        )
        self.assertRedirects(r, "/", fetch_redirect_response=False)

        r = client.get(
            reverse('state'),
        )
        self.assertTrue(r.data['already_logined'])

    def test_normal_logout(self, client=APIClient()):
        client.force_login(self.test_user)
        csrftoken = get_cookie_value(client.cookies, 'csrftoken')

        r = client.post(
            reverse('logout'),
            {'next': '/'},
            headers={'X-CSRFToken': csrftoken}
            )
        self.assertEqual(r.status_code, status.HTTP_302_FOUND)

    def test_login_out(self, client=APIClient(enforce_csrf_checks=True)):
        client.get(reverse('state'))
        self.test_normal_login(client, user_info=self.test_user_json)
        csrftoken = get_cookie_value(client.cookies, 'csrftoken')

        r = client.post(
            reverse('logout'),
            {'next': '/'},
            headers={'X-CSRFToken': csrftoken}
            )
        self.assertEqual(r.status_code, status.HTTP_302_FOUND)

    def test_totp_login(self, client=APIClient()):
        client.force_login(self.test_user)
        csrftoken = get_cookie_value(client.cookies, 'csrftoken')
        headers = {'X-CSRFToken': csrftoken}

        r = client.post(
            reverse('check-otp'),
            {'token': self.totp.now()},
            headers = headers
        )

        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = client.get(
            reverse('state')
        )
        self.assertTrue(r.data['is_verified'])

    def test_totp_login_denied_non_member(self, client=APIClient()):
        self.test_normal_login(client, generate_user_info(kaist_uid=2))
        csrftoken = get_cookie_value(client.cookies, 'csrftoken')
        headers = {'X-CSRFToken': csrftoken}

        r = client.post(
            reverse('check-otp'),
            {'token': '000000'},
            headers=headers
        )
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_totp_login_denied_replay(self, client=APIClient()):
        client.force_login(self.test_user)
        csrftoken = get_cookie_value(client.cookies, 'csrftoken')
        headers = {'X-CSRFToken': csrftoken}

        token_issued_time = datetime.datetime.now()
        used_token = self.totp.now()
        

        r = client.post(
            reverse('check-otp'),
            {'token': used_token},
            headers = headers
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = client.post(
            reverse('check-otp'),
            {'token': used_token},
            headers = headers
        )
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(datetime.datetime.now()-token_issued_time < TOTPDevice.VALID_WINDOW*2.5*datetime.timedelta(seconds=30))

    def test_totp_login_bruteforce(self, client=APIClient(), bruteforce_sec=TOTPDevice.VALID_WINDOW*75):
        print(f"A bruteforce test against totp login has started. It will take {bruteforce_sec} seconds. Please be patient.")

        client.force_login(self.test_user)
        csrftoken = get_cookie_value(client.cookies, 'csrftoken')
        headers = {'X-CSRFToken': csrftoken}

        def sleep():
            time.sleep(bruteforce_sec)

        num_attempts = 0
        num_accepted_attempts = 0

        def attempt(token):
            r = client.post(
                reverse('check-otp'),
                {'token': token},
                headers = headers
            )
            self.assertNotEqual(r.status_code, status.HTTP_200_OK)
            return r.status_code
        
        timer = threading.Thread(target=sleep)
        timer.start()
        while num_accepted_attempts < 1000000:
            timer.join(timeout=0)
            if not timer.is_alive():
                print(f"{num_accepted_attempts}/{num_attempts} attempts succeeded in {bruteforce_sec} seconds.")
                break
            reponse_code = attempt(f"{num_accepted_attempts:06}")
            if reponse_code == status.HTTP_400_BAD_REQUEST:
                num_accepted_attempts += 1
            num_attempts += 1

            
    def test_lost_totp_secret(self, client=APIClient()):
        client.force_login(self.test_user)
        csrftoken = get_cookie_value(client.cookies, 'csrftoken')
        headers = {'X-CSRFToken': csrftoken}
        GMailAPI.init()

        email = self.get_otp_mail()
        self.test_user.email = email
        self.test_user.save()

        r = client.post(
            reverse('lost-totp-secret'),
            {'email': email},
            headers = headers
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        otp = input("Enter otp: ")
        r = client.post(
            reverse('lost-totp-secret-response'),
            {'token': otp},
            headers = headers
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.totp_device.secret, r.data['secret'])


    def test_change_email(self, client=APIClient()):
        client.force_login(self.test_user)
        csrftoken = get_cookie_value(client.cookies, 'csrftoken')
        headers = {'X-CSRFToken': csrftoken}

        self.test_totp_login(client)
        GMailAPI.init()

        new_email = self.get_otp_mail()
        
        r = client.post(
            reverse('change-email'),
            {'email': new_email},
            headers = headers
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        otp = input("Enter otp: ")
        r = client.post(
            reverse('change-email-response'),
            {'token': otp},
            headers=headers
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
    
    def test_change_email_denied_replay(self, client=APIClient()):
        client.force_login(self.test_user)
        csrftoken = get_cookie_value(client.cookies, 'csrftoken')
        headers = {'X-CSRFToken': csrftoken}

        self.test_totp_login(client)
        GMailAPI.init()

        new_email = self.get_otp_mail()
        
        r = client.post(
            reverse('change-email'),
            {'email': new_email},
            headers = headers
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        otp = input("Enter otp: ")
        r = client.post(
            reverse('change-email-response'),
            {'token': otp},
            headers=headers
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = client.post(
            reverse('change-email-response'),
            {'token': otp},
            headers=headers
        )
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_change_email_max_attempts(self, client=APIClient()):
        client.force_login(self.test_user)
        csrftoken = get_cookie_value(client.cookies, 'csrftoken')
        headers = {'X-CSRFToken': csrftoken}

        self.test_totp_login(client)
        GMailAPI.init()

        new_email = self.get_otp_mail()
        
        r = client.post(
            reverse('change-email'),
            {'email': new_email},
            headers = headers
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        otp = input("Enter otp: ")
        r = client.post(
            reverse('change-email-response'),
            {'token': otp},
            headers=headers
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        r = client.post(
            reverse('change-email-response'),
            {'token': otp},
            headers=headers
        )
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        
class AuthTestLive(APILiveServerTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.totp = pyotp.TOTP(pyotp.random_base32())
        self.test_user, self.test_user_json = generate_user(totp_secret=self.totp.secret, kisa_division=1)
        self.test_user.save()
        self.test_user.refresh_from_db()
        self.session = requests.Session()
        self.session.get(self.live_server_url+reverse('state'))

    def test_normal_login(self):
        csrftoken = self.session.cookies.get('csrftoken', '')
        r = self.session.post(
            self.live_server_url+reverse('login'),
            json={'next': '/'},
            headers = {'X-CSRFToken': csrftoken},
            allow_redirects=False
            )
        self.assertEqual(r.status_code, status.HTTP_302_FOUND)
        state = parse_qs(urlparse(r.headers['Location']).query)['state'][0]

        # login-reponse POST request from iam2
        payload = {
            'result': encrypt(self.test_user_json, state),
            'state': state,
            'success': 'true'
        }
        r = self.session.post(
            self.live_server_url+reverse('login-response'),
            data=payload,
            headers = {'Origin': settings.KSSO_ORIGIN, 'X-CSRFToken': csrftoken},
            allow_redirects=False
        )
        self.assertEqual(r.status_code, status.HTTP_302_FOUND)
        self.assertEqual(r.headers['location'], "/")

        r = self.session.get(
            self.live_server_url+reverse('state'),
        )
        self.assertTrue(r.json()['already_logined'])

    def test_totp_login_concurrent_requests(self):
        self.test_user.refresh_from_db()
        self.test_normal_login()
        csrftoken = self.session.cookies.get('csrftoken', '')


        headers = {'X-CSRFToken': csrftoken}
        responses = list()
        tokens = list()

        def send_otp_login_request():
            token = self.totp.now()
            r = self.session.post(
                self.live_server_url+reverse('check-otp'),
                json={'token': token},
                headers = headers
            )
            responses.append(r)
            tokens.append(token)

        t1 = threading.Thread(target=send_otp_login_request)
        t2 = threading.Thread(target=send_otp_login_request)
        
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        self.assertEqual(tokens[0], tokens[1])
        self.assertEqual(len([r for r in responses if r.status_code == status.HTTP_200_OK]), 1)