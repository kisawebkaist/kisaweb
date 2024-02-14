import base64, datetime, logging, secrets

from email.mime.text import MIMEText

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core import signing
from django.utils.crypto import constant_time_compare
from django.db import models, transaction
from django.utils.translation import gettext as _

from googleapiclient.errors import HttpError as GHttpError

from sso.models import User
from sso.utils import GMailAPI

logger = logging.getLogger(__name__)


class User(AbstractUser):
    kaist_profile = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_kaist_profile(self):
        return self.kaist_profile
    
class SignupToken(models.Model):
    kaist_email = models.EmailField(unique=True)
    expiry = models.DateTimeField(blank=False)
    user_groups = models.IntegerField(default=0) # bitfield

    @classmethod
    def exists(cls, kaist_profile:User)->bool:
        kmail = kaist_profile.kaist_email
        query = cls.objects.filter(kaist_email=kmail)
        if query.exists():
            token = query[0]
            if token.expiry > datetime.datetime.now():
                return True
            token.delete()
        return False

    
    @classmethod
    def get(cls, kaist_profile:User):
        if cls.exists(kaist_profile):
            return cls.objects.get(kaist_email=kaist_profile.kaist_email)
        return None
    
    def use(self, request):
        user = User.objects.create_user(request.user.username, password=password, kaist_profile=kaist_profile)
        self.delete()


class MailOTP(models.Model):
    class MailOTPContext(models.TextChoices):
        SIGNUP = "SIGNUP", _("Sign up")
        MAIL_CHANGE = "MAIL_CHANGE", _("Mail change")
        FORGOT_PASSWORD = "FORGOT_PASSWORD", _("Forgot password")
    """
    {
        'data': 
        'context': <context code>
        'otp-mail': <mail used for otp>,
    }
    """
    MAX_ATTEMPT = 5
    LIFETIME = datetime.timedelta(minutes=5)
    SESSION_KEY = "mailotp_pk"
    
    CONTEXTS = {
        SIGNUP_CONTEXT,
        MAIL_CHANGE_CONTEXT,
        FORGOT_PASSWORD_CONTEXT
    }

    REASON_TXT = {
        SIGNUP_CONTEXT: "you signed up as a KISA member with this email.",
        MAIL_CHANGE_CONTEXT: "you requested to change your KISA member account mail to this email.",
        FORGOT_PASSWORD_CONTEXT: "you requested to change your KISA member account's password."
    }

    data = models.JSONField()
    otp = models.TextField()
    context = models.CharField(
        choices=MailOTPContext,
    )
    available_attempts = models.IntegerField(default=MAX_ATTEMPT)
    time_requested = models.DateTimeField()

    @classmethod
    def new(cls, data, context):
        otp = MailOTP( 
            otp=base64.b64encode(secrets.token_bytes(3)).decode(),
            data=data,
            time_requested=datetime.datetime.now()
            )
        with transaction.atomic():
            otp.save()
            otp.send_mail(cls.REASON_TXT[context])
        return otp
    

    
    @classmethod
    def verify(cls, token, otp, pk, context):
        otp_obj = MailOTP.objects.get(pk=pk)
        is_valid = True
        try:
            json_data = signing.loads(token, salt=context)
        except signing.BadSignature:
            is_valid = False

        is_valid = is_valid and constant_time_compare(otp_obj.otp, otp) and datetime.now() < otp_obj.expiry
        available_attempts = 0
        with transaction.atomic():
            otp_obj = MailOTP.objects.select_for_update().get(pk=pk)
            if is_valid:
                otp_obj.delete()
                return (json_data, 0)
            otp_obj.available_attempts -= 1
            available_attempts = otp_obj.available_attempts
            if otp_obj.available_attempts == 0:
                otp_obj.delete()
            else:
                otp_obj.save()
        return (None, available_attempts)
    
    def commit(self, request):
        # match (self.context):
        #     case self.MailOTPContext.SIGNUP:
        #         SignupToken.objects.filter(kaist_email=request.kaist_profile.kaist_email).use()
        pass
    
    # TODO: write a crontab that cleans expired mailotps and sessions
    @classmethod
    def clean_expired(cls):
        cls.objects.filter(expiry__lt=datetime.datetime.now()).delete()

    #TODO: write a better template
    def send_mail(self, reason:str):
        message = MIMEText(f"Dear KISA member,<br><br>Your instant authentication code is below for KISA services.<br>Auth Code: <b>{self.code}</b><br>This mail was sent because {reason}<br><br>Best Regards,<br>KISA Web Team", "html")
        message["To"] = self.email
        message["From"] = f"KISA Web Team <{GMailAPI.FROM_MAIL}>"
        message["Subject"] = "[No Reply] Your Personal Authentication for KISA Services"

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        try:
            GMailAPI.client.service.users().messages().send(userId="me", body=create_message).execute()
        except GHttpError as e:
            logger.exception(f"An error occured while sending a mail: {e}")


        



