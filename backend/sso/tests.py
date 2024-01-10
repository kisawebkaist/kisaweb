import json, base64
from urllib.parse import parse_qs, urlparse

from django.urls import reverse
from django.test import TestCase, Client

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from .views import SA_AES_ID_SECRET

# Create your tests here.
def generate_user_info(
    kaist_uid: int = 0, 
    country: str = 'KR',
    kaist_mail: str = 'nupjuk@kaist.ac.kr',
):
    return {
        'kaist_uid': str(abs(kaist_uid)%(10^8)).zfill(8),
        'ku_kname': 'NUPJUK KIM',
        'displayname': 'NUPJUK, KIM',
        'sn': 'KIM',
        'givenname': 'NUPJUK',
        'ku_born_date': '2024-01-01',
        'c': country,
        'ku_sex': 'M',
        'mail': kaist_mail,
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

    iv = (SA_AES_ID_SECRET+state)[80:96].encode()
    cipher = AES.new(iv, AES.MODE_CBC, iv)

    return base64.b64encode(cipher.encrypt(result_padded)).decode()

class LoginTest(TestCase):

    def test_normal_login(self):
        # fetch csrf token
        client = Client(enforce_csrf_checks=True)
        client.get('/')
        csrftoken = client.cookies['csrftoken'].value

        # login POST request
        headers = {
            'X-CSRFToken': csrftoken,
            'Host': 'localhost'
        }
        r = client.post(reverse('login'), headers=headers)
        state = parse_qs(urlparse(r.headers['Location']).query)['state'][0]

        # login-reponse POST request from iam2
        headers['Origin'] = 'https://iam2.kaist.ac.kr'
        payload = {
            'result': encrypt(generate_user_info(), state),
            'state': state,
            'success': 'true'
        }
        r = client.post(
            reverse('login-response'),
            payload,
            headers = headers
        )

        self.assertEqual(r.status_code, 302)
        self.assertNotEqual(r.headers['Location'], reverse('login-error'))