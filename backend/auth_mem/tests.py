import datetime

from django.urls import reverse

from rest_framework.test import APIClient, APITestCase
import rest_framework.status as status

from sso.models import KAISTProfile
from sso.tests import KAuthTest
from sso.tests import generate_user_info as generate_kuser_info

from .models import User


class AuthTest(APITestCase):

    def setUp(self) -> None:
        self.kaist_profile = KAISTProfile.from_info_json(generate_kuser_info())
        self.kaist_profile.last_login = datetime.datetime.now()
        self.kaist_profile.save()
        self.raw_password = "Nupjuk loves KISA. UwU"

        self.kisa_user = User.objects.create_user(
                username = "nupjuk",
                email = "kisa@kaist.ac.kr",
                kaist_profile = self.kaist_profile,
                password = self.raw_password
        )
        
        self.kisa_user.save()


    def test_normal_login(self, client=APIClient()):
        login_data = {
            "username": self.kisa_user.username,
            "password": self.raw_password,
            "next": "/"
        }
        r = client.post(reverse('login'), login_data)
        self.assertRedirects(r, "/", fetch_redirect_response=False)


    def test_normal_logout(self, client=APIClient(enforce_csrf_checks=True)):
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
        KAuthTest().test_normal_login(client)
        
        login_data = {
            "password": self.raw_password,
            "next": "/"
        }
        r = client.post(reverse('login'), login_data)
        self.assertEquals(r.status_code, status.HTTP_302_FOUND)


    def test_mail_reg(self, client=APIClient(enforce_csrf_checks=True)):
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
        try:
            from .utils import GMailAPI
            GMailAPI()
        except ValueError:
            print("GMailAPI is already initialized.")

        KAuthTest().test_normal_login(client)

        password = input("New password: ")
        r = client.post(
            reverse('change-pw'),
            { 'password': password }
        )
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        
        code = input("Verification code: ")
        r = client.post(
            reverse('attempt-pw-change'),
            {'code': code}
        )
        self.assertEquals(r.status_code, status.HTTP_200_OK)

        self.assertTrue(client.login(username=self.kisa_user.username, password=password))


