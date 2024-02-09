import threading

from django.db import models, transaction
from django.conf import settings
from django.utils.html import mark_safe
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from election.tests import test_adjusted_votes_formula

from auth_mem.models import User
from sso.models import KAISTProfile

# Create your models here.

ELECTION_MEDIA_UPLOAD_URL = 'election/img'

class Election(models.Model):
    class Meta:
        get_latest_by = "start_datetime"
        permissions = [
            ('preview_election', 'Can preview the election before it is published'),
        ] # some additional permissions for the users regarding the election
    
    start_datetime = models.DateTimeField(blank=False)
    end_datetime = models.DateTimeField(blank=False)
    intro_msg = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to=ELECTION_MEDIA_UPLOAD_URL, blank=True, null=True)
    debate_url = models.CharField(max_length=512, blank=True, null=True) 
    slug = models.SlugField(max_length=50) # the slug will usually be the same as str(self)
    is_open_public = models.BooleanField(default=False)
    """if the election information is visible to the public"""
    results_out = models.BooleanField(default=False)
    """if the election results are visible to the public"""

    # adjusted_votes_formula = models.TextField(blank=False, null=True, 
    #     default='((kivm) / (kiva) + (kovm + nkvm) / (kova + nkva)) * 0.5', 
    #     help_text='The variables allowed to be used: kiva, kivm, kova, kovm, nkva and nkvm'
    # ) # the formula used to calculate the adjusted votes
    # # accounts for the contribution of the kisa (in/out of debate) members, general votes etc.

    def __str__(self):
        month = int(self.start_datetime.strftime('%m'))
        year = self.start_datetime.strftime('%Y')
        if month < 8:
            semester = 'Spring'
        else:
            semester = 'Fall'
        return f'{semester}{year}'

    def clean(self):
        # check if the adjusted votes formula is valid
        # if not, raise a validation error
        adjusted_votes_formula = self.adjusted_votes_formula
        
        formula_test_result = test_adjusted_votes_formula(adjusted_votes_formula)
        if formula_test_result != 'OK':
            raise ValidationError(formula_test_result)
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # convert the youtube video url into an embed url
        if self.debate_url:
            if 'https://www.youtube.com/watch?v=' in self.debate_url:
                self.debate_url = self.debate_url.replace(
                    'https://www.youtube.com/watch?v=',
                    'https://www.youtube.com/embed/'
                )
            if 'https://youtu.be/' in self.debate_url:
                self.debate_url = self.debate_url.replace(
                    'https://youtu.be/',
                    'https://www.youtube.com/embed/'
                )
        
        # get rid of trailing and leading spaces in the email lists
        self.kisa_member_email_list = self.kisa_member_email_list.strip()
        self.kisa_in_debate_member_email_list = self.kisa_in_debate_member_email_list.strip()
        
        super().save(*args, **kwargs)

    def image_tag(self):
        # used in the admin page and election page to display the image
        if not self.image:
            path = '/static/img/election-default-dist.png'
        else:
            path = self.image.url
        return mark_safe(f'<img src="{path}" alt="Election Image" width="150px" height="150px" />')

        

class Candidate(models.Model):
    class Meta:
        index_together = ('account', 'election')
    # candidate data
    account = models.ForeignKey(User, on_delete=models.PROTECT)
    election = models.ForeignKey(Election, on_delete=models.PROTECT)
    manifesto = models.JSONField()
    speech_url = models.CharField(max_length=512, blank=True, null=True)
    kisa_history = models.JSONField()
    image = models.ImageField(upload_to=ELECTION_MEDIA_UPLOAD_URL, blank=True, null=True)
    slug = models.SlugField(max_length=120)
    is_open_public = models.BooleanField(default=False)
    num_votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{str(self.election)}-{self.acount.full_name.replace(' ', '-')}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # convert the youtube video url into an embed url
        if self.speech_url and 'https://www.youtube.com/watch?v=' in self.speech_url:
            if 'https://www.youtube.com/watch?v=' in self.speech_url:
                self.speech_url = self.speech_url.replace(
                    'https://www.youtube.com/watch?v=',
                    'https://www.youtube.com/embed/'
                )
            if 'https://youtu.be/' in self.speech_url:
                self.speech_url = self.speech_url.replace(
                    'https://youtu.be/',
                    'https://www.youtube.com/embed/'
                )
        super().save(*args, **kwargs)

    def image_tag(self):
        # used in the admin page and election page to display the image
        if not self.image:
            path = '/static/img/candidate-default-dist.png'
        else:
            path = self.image.url
        return mark_safe(f'<img src="{path}" alt="Candidate Image"/>')


class Vote(models.Model):
    class Meta:
        index_together = ('user', 'candidate')
    user = models.ForeignKey(KAISTProfile, on_delete=models.PROTECT, related_name='votes') # the user who votes
    candidate = models.ForeignKey(Candidate, on_delete=models.PROTECT, related_name='voters') # the candidate who is voted
    vote_type = models.BooleanField(default=True) 


class DebateAttendance(models.Model):
    class Meta:
        index_together = ('user', 'election')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    election = models.ForeignKey(Election, on_delete=models.PROTECT)

    @staticmethod
    def from_mail_list(cls, mails):
        attendance_list = []
        for i in mails:
            attendance_list.append(User.objects.get(kaist_profile__kaist_email=i))
            # check the length of result because we don't know whether kaist gives new members deactivated mails
        return attendance_list

class VotingExceptionToken(models.Model):
    user = models.ForeignKey(KAISTProfile, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)

# TODO: write a SIGINT handler that waits for threads other than the main thread
@receiver(models.signals.post_save, sender=Vote)
def update_num_votes(sender, **kwargs):
    def do_async(vote):
        vote_weight = 1
        member = User.objects.filter(kaist_profile=vote.user, is_active=True)
        is_kisa = member.exists()
        if (is_kisa and VotingExceptionToken.objects.filter(election=Election.objects.latest(), user=member).exists()):
            vote_weight = 2
        
        with transaction.atomic():
            del vote.candidate.num_votes
            vote.candidate.num_votes += vote_weight
            vote.candidate.save()

    if sender.vote_type:
        threading.Thread(target=do_async, args=[sender]).start()
