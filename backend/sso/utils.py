import base64, json, logging, secrets, os

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import EmailValidator
from django.utils.crypto import constant_time_compare

from rest_framework.exceptions import ParseError, PermissionDenied, ValidationError

from google.auth.transport.requests import Request as GRequest
from google.auth.exceptions import RefreshError as GRefreshError
from google.oauth2.credentials import Credentials as GCredentials
from google_auth_oauthlib.flow import InstalledAppFlow as GInstalledAppFlow
from googleapiclient.discovery import build as gbuild

logger = logging.getLogger(__name__)
email_validator = EmailValidator()
username_validator = UnicodeUsernameValidator()

class GMailAPI:
    """
    A singleton class for generating gmail api client
    """
    GSCOPES_REQUIRED = [
    'https://www.googleapis.com/auth/gmail.send',
    ]
    FROM_MAIL = "kisa.web@gmail.com"
    client = None

    def __init__(self):
        if GMailAPI.client is not None:
            raise ValueError()
        
        GMailAPI.client = self

        self.credentials = None
        try:
            self.credentials = GCredentials.from_authorized_user_file("gmail-api-token.json")
            if not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    self.credentials.refresh(GRequest())
                with open("gmail-api-token.json", "w+") as token:
                    token.write(self.credentials.to_json())
            self.service = gbuild('gmail', 'v1', credentials=self.credentials)
        except GRefreshError as e:
            logger.exception(f"Token refresh failed: {e}")

    @classmethod
    def init(cls):
        if cls.client is None:
            cls.client = GMailAPI()

    @classmethod
    def get_api_token(cls):
        flow = GInstalledAppFlow.from_client_secrets_file(
            "sso/client-secrets.json", cls.GSCOPES_REQUIRED
        )
        creds = flow.run_local_server(port=0)
        with open("gmail-api-token.json", "w+") as token:
            token.write(creds.to_json())
