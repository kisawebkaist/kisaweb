from django import forms
from django.db import models
from django.conf import settings
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
    date = models.DateField(auto_now_add=True, null=True)

    EMBED_VIDEO_RATIO_CHOICES = [
        ('21by9', '21by9'),
        ('16by9', '16by9'),
        ('4by3', '4by3'),
        ('1by1', '1by1'),
    ]
    embed_video_ratio = models.CharField(max_length=10, default='16by9', choices=EMBED_VIDEO_RATIO_CHOICES)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.speech_url and 'https://www.youtube.com/watch?v=' in self.speech_url:
            self.speech_url = self.speech_url.replace(
                'https://www.youtube.com/watch?v=',
                'https://www.youtube.com/embed/'
            )
        super().save(*args, **kwargs)

    def image_tag(self):
        if not self.image:
            path = '/static/img/candidate-default-dist.png'
        else:
            path = self.image.url
        return mark_safe(f'<img src="{path}" alt="Candidate Image"/>')

    def change_embed_ratio(self, ratio):
        lst = [i[0] for i in self.EMBED_VIDEO_RATIO_CHOICES]
        if ratio in lst:
            self.embed_video_ratio = ratio
            self.save(update_fields=['embed_video_ratio'])
        else:
            return 'Error'



class Election(models.Model):
    class Meta:
        permissions = [
            ('see_election_results', 'Can view election results anytime'),
            ('preview_election', 'Can preview the election before it is published'),
        ]
    
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    candidates = models.ManyToManyField(Candidate, blank=False)
    intro_msg = HTMLField()
    instructions = HTMLField()
    image = models.ImageField(upload_to=ELECTION_MEDIA_UPLOAD_URL, blank=True, null=True)
    debate_url = models.CharField(max_length=512, blank=True, null=True)
    is_open_public = models.BooleanField(default=False, null=True)
    results_out = models.BooleanField(default=False, null=True)
    kisa_member_email_list = models.TextField(blank=True)

    EMBED_VIDEO_RATIO_CHOICES = [
        ('21by9', '21by9'),
        ('16by9', '16by9'),
        ('4by3', '4by3'),
        ('1by1', '1by1'),
    ]
    embed_video_ratio = models.CharField(max_length=10, default='16by9', choices=EMBED_VIDEO_RATIO_CHOICES)

    def __str__(self):
        month = int(self.start_datetime.strftime('%m'))
        year = self.start_datetime.strftime('%Y')
        if month < 8:
            semester = 'Spring'
        else:
            semester = 'Fall'
        return f'{semester} {year}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.debate_url and 'https://www.youtube.com/watch?v=' in self.debate_url:
            self.debate_url = self.debate_url.replace(
                'https://www.youtube.com/watch?v=',
                'https://www.youtube.com/embed/'
            )
        super().save(*args, **kwargs)

    def image_tag(self):
        if not self.image:
            path = '/static/img/election-default-dist.png'
        else:
            path = self.image.url
        return mark_safe(f'<img src="{path}" alt="Election Image" width="150px" height="150px" />')

    def change_embed_ratio(self, ratio):
        lst = [i[0] for i in self.EMBED_VIDEO_RATIO_CHOICES]
        if ratio in lst:
            self.embed_video_ratio = ratio
            self.save(update_fields=['embed_video_ratio'])
        else:
            return 'Error'

'''
    class "Voter" is designed for extending the "User"
    model to be associated with a vote.
'''

class Voter(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='votes')
    voted_candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='voters')
    voted_election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='voters')
    vote_type = models.CharField(max_length=10, blank=True)
    is_kisa = models.BooleanField(default=False)


@receiver(models.signals.post_save, sender=Voter)
def update_voter(sender, instance, *args, **kwargs):
    voted_election = instance.voted_election
    kaist_email = instance.user.kaist_email
    if kaist_email is None: 
        assert(instance.user.is_staff) # The opposite case should never happen
        kaist_email = 'kisa@kaist.ac.kr'
    if instance.is_kisa:
        if voted_election.kisa_member_email_list.find(kaist_email) == -1:
            voted_election.kisa_member_email_list = f'{voted_election.kisa_member_email_list.strip()}\n{kaist_email}'
    else:
        voted_election.kisa_member_email_list = voted_election.kisa_member_email_list.replace(f'{kaist_email}\n', '')
        voted_election.kisa_member_email_list = voted_election.kisa_member_email_list.replace(f'\n{kaist_email}', '')
        voted_election.kisa_member_email_list = voted_election.kisa_member_email_list.replace(f'{kaist_email}', '')

    voted_election.save(update_fields=['kisa_member_email_list'])

