import datetime

from django.contrib.auth.hashers import make_password
from django.urls import reverse

from rest_framework.test import APIClient, APITestCase
import rest_framework.status as status

from sso.models import KAISTProfile
from sso.tests import KAuthTest
from sso.tests import generate_user_info as generate_kuser_info

from .models import User, SignupToken


class AuthTest(APITestCase):
    test_email = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_email = input("Enter the mail to be used to receive otps for testing.\n").strip()

    def setUp(self) -> None:
        self.kaist_profile = KAISTProfile.from_info_json(generate_kuser_info(kaist_email=self.test_email))
        self.kaist_profile.last_login = datetime.datetime.now()
        self.kaist_profile.save()
        self.raw_password = "Nupjuk loves KISA. :3"

        self.kisa_user = User(
                username = "nupjuk",
                email = self.test_email,
                kaist_profile = self.kaist_profile,
                password = make_password(self.raw_password),
        )
        self.kisa_user.full_clean()

    def create_test_account(self):
        self.kisa_user.save()


    def test_normal_login(self, client=APIClient()):
        self.create_test_account()

        login_data = {
            "username": self.kisa_user.username,
            "password": self.raw_password,
            "next": "/"
        }
        r = client.post(reverse('login'), login_data)
        self.assertRedirects(r, "/", fetch_redirect_response=False)


    def test_normal_logout(self, client=APIClient()):
        self.create_test_account()

        client.get(reverse('state'))
        
        client.login(
            username=self.kisa_user.username,
            password=self.raw_password
        )
        headers = {
            'X-CSRFToken': client.cookies['csrftoken'].value
        }
        
        r = client.post(reverse('logout'), headers=headers)
        self.assertRedirects(r, "/", fetch_redirect_response=False)


    def test_normal_login_after_klogin(self, client=APIClient()):
        self.create_test_account()

        KAuthTest().test_normal_login(client, generate_kuser_info(kaist_email=self.test_email))
        
        login_data = {
            "password": self.raw_password,
            "next": "/"
        }
        r = client.post(reverse('login'), login_data)
        self.assertEquals(r.status_code, status.HTTP_302_FOUND)


    def test_mail_reg(self, client=APIClient()):
        self.create_test_account()

        client.get(reverse('state'))
        try:
            from .utils import GMailAPI
            GMailAPI()
        except ValueError:
            print("GMailAPI is already initialized.")
        
        client.login(
            username=self.kisa_user.username,
            password=self.raw_password
        )
        headers = {
            'X-CSRFToken': client.cookies['csrftoken'].value
        }

        r = client.post(
            reverse('register-mail'),
            { 'email': self.kisa_user.email },
            headers = headers
        )
        
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        code = input("Verification code: ")

        r = client.post(
            reverse('attempt-mail-reg'),
            { 'code': code },
            headers = headers
        )

        self.assertEquals(r.status_code, status.HTTP_200_OK)


    def test_mail_password_change(self, client=APIClient()):
        self.create_test_account()

        try:
            from .utils import GMailAPI
            GMailAPI()
        except ValueError:
            print("GMailAPI is already initialized.")

        KAuthTest().test_normal_login(client)

        self.raw_password = input("New password: ")
        r = client.post(
            reverse('change-pw'),
            { 'password': self.raw_password }
        )
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        
        code = input("Verification code: ")
        r = client.post(
            reverse('attempt-pw-change'),
            {'code': code}
        )
        self.assertEquals(r.status_code, status.HTTP_200_OK)

        self.assertTrue(client.login(username=self.kisa_user.username, password=self.raw_password))

    def test_signup(self, client=APIClient()):
        KAuthTest().test_normal_login(client, generate_kuser_info(kaist_email=self.test_email))

        token = SignupToken.objects.create(kaist_email=self.kaist_profile.kaist_email, expiry=datetime.datetime.now()+datetime.timedelta(days=1), user_groups=0)

        r = client.post(
            reverse('signup'),
            {
                'username': self.kisa_user.username,
                'password': self.raw_password
            }
        )

        self.assertEquals(r.status_code, status.HTTP_200_OK)
        self.assertTrue(client.login(username=self.kisa_user.username, password=self.raw_password))
