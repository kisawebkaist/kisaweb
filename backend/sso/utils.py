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
from googleapiclient.errors import HttpError as GHttpError

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
        except GHttpError as e:
            logger.exception(f"An error occurred while initializing gmail api client: {e}")

    @classmethod
    def init(cls):
        if cls.client is None:
            cls.client = GMailAPI()

class MailOTPContext:
    ALL = dict()
    def __init__(self, slug, reason_txt, validate):
        MailOTPContext.ALL[slug] = self
        self.slug = slug
        self.salt = "MailOTP."+slug+"_Context"
        self.validate = validate
        self.reason_txt = reason_txt

def validate_mail_signup_data(data):
    try:
        username_validator(data['username'])
        validate_password(data['password'])
    except ValueError:
        raise ParseError()
    except DjangoValidationError as e:
        raise ValidationError(e.message, e.code)
    return {
        'email': data['email']
    }

def validate_mail_change_data(data):
    return {
        'email': data['email']
    }
def validate_password_change_data(data):
    password = data['password']
    try:
        validate_password(password)
    except DjangoValidationError as e:
        raise ValidationError(e.error_dict, e.code)

MailOTPContext(
    "Signup",
    "you signed up as a KISA member with this email.",
    validate=validate_mail_signup_data
)
