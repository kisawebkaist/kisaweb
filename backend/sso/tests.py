import json, base64
from urllib.parse import urlencode
from urllib.parse import parse_qs, urlparse

from django.conf import settings
from django.urls import reverse

from rest_framework.test import APIClient, APITestCase
import rest_framework.status as status

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from .middleware import SA_AES_ID_SECRET


def generate_user_info(
    kaist_uid: int = 1, 
    country: str = 'KR',
    kaist_email: str = 'nupjuk@kaist.ac.kr',
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

    iv = (SA_AES_ID_SECRET+state)[80:96].encode()
    cipher = AES.new(iv, AES.MODE_CBC, iv)

    return base64.b64encode(cipher.encrypt(result_padded)).decode()

class KAuthTest(APITestCase):

    def test_normal_login(self, client=APIClient(), user_info=generate_user_info()):
        r = client.post(
            reverse('klogin'),
            {'next': '/'},
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
            reverse('klogin-response'),
            urlencode(payload),
            headers = {'Origin': settings.KSSO_ORIGIN},
            content_type='application/x-www-form-urlencoded'
        )
        self.assertRedirects(r, "/", fetch_redirect_response=False)

    def test_normal_logout(self, client=APIClient()):
        self.test_normal_login(client)

        r = client.post(
            reverse('klogout'),
            {'next': '/'}
            )
        self.assertEqual(r.status_code, status.HTTP_302_FOUND)
