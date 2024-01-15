import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from sso.models import KAISTProfile

class User(AbstractUser):
    kaist_profile = models.OneToOneField(KAISTProfile, on_delete=models.CASCADE)

    def get_kaist_profile(self):
        return self.kaist_profile
    
class SignupToken(models.Model):
    kaist_email = models.EmailField(unique=True)
    expiry = models.DateTimeField(blank=False)
    user_groups = models.IntegerField() # bitfield

    @classmethod
    def exists(cls, kaist_profile:KAISTProfile)->bool:
        kmail = kaist_profile.kaist_email
        if cls.objects.exists(kaist_email=kmail):
            token = cls.objects.get(kaist_email=kmail)
            if token.expiry > datetime.datetime.now():
                return True
            token.delete()
        return False

    
    @classmethod
    def get(cls, kaist_profile:KAISTProfile):
        if cls.exists(kaist_profile):
            return cls.objects.get(kaist_email=kaist_profile.kaist_email)
        return None
    
    def use(self, username, password):
        user = User.objects.create_user(username, password=password)
        user.date_joined = datetime.date.today()
        user.save()
        self.delete()
