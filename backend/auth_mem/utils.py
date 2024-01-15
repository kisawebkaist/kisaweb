import base64, json, logging, secrets, os
from email.message import EmailMessage
from typing import Union

from django.utils.crypto import constant_time_compare

from google.auth.transport.requests import Request as GRequest
from google.oauth2.credentials import Credentials as GCredentials
from google_auth_oauthlib.flow import InstalledAppFlow as GInstalledAppFlow
from googleapiclient.discovery import build as gbuild
from googleapiclient.errors import HttpError as GHttpError

logger = logging.getLogger(__name__)

class GMailAPI:
    """
    A singleton class for generating gmail api client
    """
    GSCOPES_REQUIRED = [
    'https://www.googleapis.com/auth/gmail.send',
    ]
    CLIENT_SECRETS_FILE = 'auth_mem/client-secrets.json'
    FROM_MAIL = "kisa.web@gmail.com"
    client = None

    def __init__(self):
        if GMailAPI.client is not None:
            raise ValueError()
        
        GMailAPI.client = self

        self.credentials = None
        try:
            if os.path.exists("gmail-api-token.json"):
                self.credentials = GCredentials.from_authorized_user_file("gmail-api-token.json")
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    self.credentials.refresh(GRequest())
                else:
                    flow = GInstalledAppFlow.from_client_secrets_file(
                        self.CLIENT_SECRETS_FILE, self.GSCOPES_REQUIRED
                    )
                    self.credentials = flow.run_local_server(port=0)
                with open("gmail-api-token.json", "w+") as token:
                    token.write(self.credentials.to_json())

            self.service = gbuild('gmail', 'v1', credentials=self.credentials)
        except GHttpError as e:
            logger.exception(f"An error occurred while initializing gmail api client: {e}")

class MailVerificationCode:
    """
    A class for generating, storing, and sending mail-verification-codes
    - Make sure that it is a valid mail before generating a verification code
    - The number of checks may be subject to race conditions and become a little more than MAX_ATTEMPTS but that's ok
    """
    MAX_ATTEMPTS = 6
    PW_CHANGE = 'pw'
    REGISTRATION = 'reg'

    def __init__(self, code:str, email:str, available_attempts:str) -> None:
        self.code = code
        self.email = email
        self.available_attempts = available_attempts
        self.extra_info = None

    @classmethod
    def new(cls, email):
        return MailVerificationCode(base64.b64encode(secrets.token_bytes(3)).decode(), email, cls.MAX_ATTEMPTS)

    @classmethod
    def __get_session_key(cls, context:str):
        return 'mail_ver_'+context
    
    @classmethod
    def __attempt_context(cls, session, code, context):
        session_key = cls.__get_session_key(context)
        data = session.get(session_key)
        if data is None:
            return (None, 0)
        
        code_obj = cls.deserialize(data)
        if not constant_time_compare(code_obj.code, code):
            code_obj.available_attempts -= 1

            if code_obj.available_attempts == 0:
                del session[session_key]
            else:
                code_obj.saveForPasswordChange(session)

            return (None, code_obj.available_attempts)
        
        del session[session_key]
        return (code_obj, 0)
    
    @classmethod
    def attempt_pw(cls, session, code:str)->(Union[str, None], int):
        """
        Returns (mail, num of available attempts)
        - if the attempt fails, mail will be None
        """
        code_obj, num_avai_attempts = cls.__attempt_context(session, code, cls.PW_CHANGE)
        if code_obj is None:
            return (None, num_avai_attempts)
        return (code_obj.extra_info['password'], num_avai_attempts)
    
    @classmethod
    def attempt_reg(cls, session, code:str)->(Union[str, None], int):
        """
        Return (password, num of available attempts)
        - if the attempt fails, password will None
        """
        code_obj, num_avai_attempts =  cls.__attempt_context(session, code, cls.REGISTRATION)
        if code_obj is None:
            return (None, num_avai_attempts)
        return (code_obj.email, num_avai_attempts)

    @classmethod
    def deserialize(cls, json_str):
        dict_obj = json.loads(json_str)
        code_obj = cls(dict_obj['code'], dict_obj['code'], dict_obj['available_attempts'])
        if 'extra_info' in dict_obj and dict_obj['extra_info'] is not None:
            code_obj.extra_info = dict_obj['extra_info']
        return code_obj
    
    def saveForMailRegistraion(self, session, username):
        session[self.__get_session_key(self.REGISTRATION)] = self.serialize()
        self.send_mail(f"you requested to register this mail for a KISA account with username {username}.")

    def saveForPasswordChange(self, session, password):
        self.extra_info = {'password': password}
        session[self.__get_session_key(self.PW_CHANGE)] = self.serialize()
        self.send_mail("you requested for a password change for your KISA account.")

    def serialize(self):
        return json.dumps(
            {
                'code': self.code,
                'email': self.email,
                'available_attempts': self.available_attempts,
                'extra_info': getattr(self, 'extra_info', None)
            }
        )
    
    #TODO: write a better template
    def send_mail(self, reason:str):
        message = EmailMessage()
        message["To"] = self.email
        message["From"] = f"KISA Web Team <{GMailAPI.FROM_MAIL}>"
        message["Subject"] = "[No Reply] Your Personal Authentication for KISA Services"
        message.set_content(f"Dear KISA member,\nYour instant authentication code is below for KISA services.\nAuth Code: {self.code}\nThis mail was sent because {reason}\nBest Regards,\nKISA Web Team")

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        try:
            GMailAPI.client.service.users().messages().send(userId="me", body=create_message).execute()
        except GHttpError as e:
            logger.exception(f"An error occured while sending a mail: {e}")