import datetime, threading

from django.db import models, transaction
from django.conf import settings
from django.dispatch import receiver

from sso.models import User

ELECTION_MEDIA_UPLOAD_URL = 'election/img'

class Election(models.Model):
    class Meta:
        get_latest_by = "start_datetime"
        permissions = [
            ('preview_election', 'Can preview the election before it is published'),
        ] # some additional permissions for the users regarding the election
    
    start_datetime = models.DateTimeField(default=datetime.datetime.now, blank=True)
    end_datetime = models.DateTimeField()
    intro_msg = models.JSONField(default=dict, blank=True)
    instructions = models.JSONField(default=dict, blank=True)
    image = models.ImageField(upload_to=ELECTION_MEDIA_UPLOAD_URL, blank=True, null=True)
    debate_url = models.CharField(max_length=512, blank=True, null=True) 
    slug = models.SlugField(max_length=50, blank=True) # the slug will usually be the same as str(self)
    is_open_public = models.BooleanField(default=False, blank=True)
    """if the election information is visible to the public"""
    results_out = models.BooleanField(default=False)
    """if the election results are visible to the public"""

    def slugifiy(self):
        ideal = str(self)
        if not Election.objects.filter(slug=ideal).exists():
            return ideal
        attempt = 0
        while True:
            test = f"{ideal}_{str(attempt)}"
            if not Election.objects.filter(slug=test).exists():
                return test
            attempt += 1

    def __str__(self):
        month = int(self.start_datetime.strftime('%m'))
        year = self.start_datetime.strftime('%Y')
        if month < 8:
            semester = 'Spring'
        else:
            semester = 'Fall'
        return f'{semester}{year}'

    def clean(self):
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
        if self.slug is None or self.slug == "":
            self.slug = self.slugifiy()
        return super().clean() 

class Candidate(models.Model):
    class Meta:
        index_together = ('account', 'election')
    # candidate data
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, default=Election.objects.latest)
    manifesto = models.JSONField(default=dict)
    speech_url = models.CharField(max_length=512, blank=True, null=True)
    kisa_history = models.JSONField(default=dict, blank=True)
    image = models.ImageField(upload_to=ELECTION_MEDIA_UPLOAD_URL, blank=True, null=True)
    slug = models.SlugField(max_length=120, blank=True)
    is_open_public = models.BooleanField(default=False)
    num_votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{str(self.election)}_{self.slug}"
    
    def slugify(self):
        ideal = self.account.get_full_name().replace(' ', '-')
        if not Candidate.objects.filter(election=self.election, slug=ideal).exists():
            return ideal
        attempt = 0
        while True:
            test = f"{ideal}_{str(attempt)}"
            if not Candidate.objects.filter(election=self.election, slug=test).exists():
                return test
            attempt += 1
            
    def clean(self):
        if self.slug is None or self.slug == "":
            self.slug = self.slugify()
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
        return super().clean()


class Vote(models.Model):
    class Meta:
        index_together = ('user', 'candidate')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='votes') # the user who votes
    candidate = models.ForeignKey(Candidate, on_delete=models.PROTECT, related_name='voters') # the candidate who is voted
    vote_type = models.BooleanField(default=True) 

    working_theads = []

class DebateAttendance(models.Model):
    class Meta:
        index_together = ('user', 'election')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    election = models.ForeignKey(Election, on_delete=models.PROTECT)

    @classmethod
    def save_from_mail_list(cls, mails):
        users = []
        for i in mails:
            users.append(User.objects.get(kaist_email=i))
        election = Election.objects.latest()
        for user in users:
            if not user.is_kisa():
                raise ValueError(user)
            DebateAttendance(user=user, election=election).save()

class VotingExceptionToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, default=Election.objects.latest)

# TODO: write a SIGINT handler that waits for threads other than the main thread
@receiver(models.signals.post_save, sender=Vote)
def update_num_votes(sender, **kwargs):
    def do_async(vote):
        vote_weight = 1
        election = vote.candidate.election

        if (vote.user.is_kisa() and DebateAttendance.objects.filter(election=election, user=vote.user).exists()):
            vote_weight = 2
        
        with transaction.atomic():
            candidate = Candidate.objects.select_for_update().get(pk=vote.candidate.pk)
            candidate.num_votes += vote_weight
            candidate.save()

    if sender.vote_type:
        thread = threading.Thread(target=do_async, args=[sender])
        Vote.working_theads.append(thread)
        thread.start()
