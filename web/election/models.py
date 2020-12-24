from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.dispatch import receiver
from django.db.models.signals import post_save

from tinymce.models import HTMLField

# Create your models here.

ELECTION_MEDIA_UPLOAD_URL = 'election/img'

class Candidate(models.Model):
    name = models.CharField(max_length=100, default='')
    manifesto = HTMLField()
    speech_url = models.CharField(max_length=512, blank=True, null=True)
    kisa_history = HTMLField()
    image = models.ImageField(upload_to=ELECTION_MEDIA_UPLOAD_URL, blank=True, null=True)

    def __str__(self):
        return self.name

    def image_tag(self):
        if not self.image:
            path = '/static/img/candidate-default-dist.png'
        else:
            path = self.image.url
        return mark_safe(f'<img src="{path}" alt="Candidate Image" width="200" height="200" />')

<<<<<<< HEAD
    def vote(self):
        self.votes += 1
        self.save(update_fields=['votes'])

    def remove_vote(self):
        self.votes -= 1
        self.save(update_fields=['votes'])

    def vote_yes(self):
        self.yes += 1
        self.save(update_fields=['yes'])

    def vote_no(self):
        self.no += 1
        self.save(update_fields=['no'])

    def change_embed_ratio(self, ratio):
        lst = [i[0] for i in self.EMBED_VIDEO_RATIO_CHOICES]
        if ratio in lst:
            self.embed_video_ratio = ratio
            self.save(update_fields=['embed_video_ratio'])
        else:
            return 'Error'


||||||| 4e9c7df
    def vote(self):
        self.votes = models.F('votes') + .5
        self.save(update_fields=['votes'])

    def vote_yes(self):
        self.yes = models.F('yes') + .5
        self.save(update_fields=['yes'])

    def vote_no(self):
        self.no = models.F('no') + .5
        self.save(update_fields=['no'])

    def change_embed_ratio(self, ratio):
        lst = [i[0] for i in self.EMBED_VIDEO_RATIO_CHOICES]
        if ratio in lst:
            self.embed_video_ratio = ratio
            self.save(update_fields=['embed_video_ratio'])
        else:
            return 'Error'


=======
>>>>>>> 1b438b8a24d083a4fb94f4f339788666b04b80f7

class Election(models.Model):
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    candidates = models.ManyToManyField(Candidate, blank=False)
    intro_msg = HTMLField()
    instructions = HTMLField()
    image = models.ImageField(upload_to=ELECTION_MEDIA_UPLOAD_URL, blank=True, null=True)

    def __str__(self):
        month = int(self.start_datetime.strftime('%m'))
        year = self.start_datetime.strftime('%Y')
        if month < 8:
            semester = 'Spring'
        else:
            semester = 'Fall'
        return f'{semester} {year}'

    def image_tag(self):
        if not self.image:
            path = '/static/img/election-default-dist.png'
        else:
            path = self.image.url
        return mark_safe(f'<img src="{path}" alt="Election Image" width="150px" height="150px" />')

'''
    class "Voter" is designed for extending the "User"
    model to be associated with a vote.
'''

class Voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='voter')
    voted_candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='voters')
    vote_type = models.CharField(max_length=10, blank=True)
    is_kisa = models.BooleanField(default=False)


@receiver(models.signals.post_delete, sender=Voter)
def delete_voter(sender, instance, *args, **kwargs):
    voted_candidate = instance.voted_candidate
    voted_candidate.remove_vote()
