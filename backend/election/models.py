import datetime, threading

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import models, transaction
from django.conf import settings
from django.dispatch import receiver
from django.utils.translation import gettext as _

from rest_framework.exceptions import ParseError

from sso.models import User
from core.utils import housekeeping_signal, DraftJSEditorField

ELECTION_MEDIA_UPLOAD_URL = 'election/img'

class Election(models.Model):
    CACHE_TTL = datetime.timedelta(minutes=10)
    class Meta:
        get_latest_by = "start_datetime"
        permissions = [
            ('preview_election', 'Can preview the election before it is published'),
        ] # some additional permissions for the users regarding the election

    start_datetime = models.DateTimeField(default=datetime.datetime.now, blank=True)
    end_datetime = models.DateTimeField()
    intro_msg = DraftJSEditorField(default=dict, blank=True)
    instructions = DraftJSEditorField(default=dict, blank=True)
    image = models.ImageField(upload_to=ELECTION_MEDIA_UPLOAD_URL, blank=True, null=True)
    debate_url = models.CharField(max_length=512, blank=True, null=True)
    slug = models.SlugField(max_length=50, blank=True, help_text="You can leave this blank.") # the slug will usually be the same as str(self)
    is_open_public = models.BooleanField(default=False, blank=True)
    """if the election information is visible to the public"""
    results_out = models.BooleanField(default=False, blank=True)
    """if the election results are visible to the public"""
    results_cache_datetime = models.DateTimeField(default=datetime.datetime.now, blank=True)
    results_archived = models.BooleanField(default=False, blank=True)

    def get_election_type(self):
        return 'multi' if Candidate.objects.filter(election=self).count()>1 else 'single'

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

    def update_election_result_cache(self, force=False):
        # caching for both performance and voters' privacy
        with transaction.atomic():
            locked_self = Election.objects.select_for_update().get(pk=self.pk)
            now = datetime.datetime.now()

            if not force and (now-locked_self.results_cache_datetime < locked_self.CACHE_TTL or locked_self.results_archived):
                return

            counter = dict()
            candidates = Candidate.objects.filter(election=locked_self).all()
            for candidate in candidates:
                counter[candidate] = 0
            for vote in Vote.objects.filter(election=locked_self, vote_type=True).all():
                counter[vote.candidate] += 1
                if (vote.user.is_kisa() and DebateAttendance.objects.filter(election=locked_self, user=vote.user).exists()):
                    counter[vote.candidate] += 1
            for candidate in candidates:
                candidate.num_votes = counter[candidate]
                candidate.save()

            locked_self.results_cache_datetime = datetime.datetime.now()
            locked_self.save()

    def archive(self):
        """When the election is over, we can just save the number of votes and delete the other information for users' privacy."""
        with transaction.atomic():
            self.update_election_result_cache()
            for vote in Vote.objects.filter(election=self):
                vote.delete()
            for debate_attendance in DebateAttendance.objects.filter(election=self):
                debate_attendance.delete()
            for voting_exeception in VotingExceptionToken.objects.filter(election=self):
                voting_exeception.delete()
            self.results_archived = True
            self.save()

    @classmethod
    def current_or_error(cls):
        elections = cls.objects.order_by('-start_datetime').all()
        now = datetime.datetime.now()
        for election in elections:
            if election.start_datetime <= now and election.end_datetime >= now:
                return election
        raise ParseError(_("There is no ongoing election."))


class Candidate(models.Model):
    class Meta:
        unique_together = ('account', 'election')
    # candidate data
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, default=Election.objects.latest)
    manifesto = models.JSONField(default=dict, blank=True)
    speech_url = models.CharField(max_length=512, blank=True, null=True)
    kisa_history = models.JSONField(default=dict, blank=True)
    image = models.ImageField(upload_to=ELECTION_MEDIA_UPLOAD_URL, blank=True, null=True)
    slug = models.SlugField(max_length=120, blank=True)
    """the candidate slugs should be unique for each election"""
    is_open_public = models.BooleanField(default=False)
    num_votes = models.PositiveIntegerField(default=0)
    """this should be modified only by Election.update_election_result_cache"""

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
        unique_together = ('user', 'election') # this is here to prevent subtle insert-race-conditions in voting without locking the whole table
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True)
    vote_type = models.BooleanField(default=True)

    def clean(self):
        if self.candidate.election != self.election:
            raise DjangoValidationError(
                _("Invalid candidate: %(candidate)s"),
                params={"candidate": str(self.candidate)}
            )
        return super().clean()

    def __str__(self) -> str:
        return f"{str(self.user)}'s vote for {str(self.election)}"

class DebateAttendance(models.Model):
    class Meta:
        unique_together = ('user', 'election')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)

    @classmethod
    def save_from_mail_list(cls, mails):
        users = []
        for i in mails:
            users.append(User.objects.get(kaist_email=i))
        election = Election.objects.latest()
        with transaction.atomic():
            for user in users:
                if not user.is_kisa():
                    raise ValueError(user)
                DebateAttendance(user=user, election=election).save()

class VotingExceptionToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, default=Election.objects.latest)

@receiver(housekeeping_signal)
def update_election_cache(sender, **kwargs):
    for election in Election.objects.all():
        election.update_election_result_cache()
