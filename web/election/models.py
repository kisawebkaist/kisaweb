from django.db import models
from django.conf import settings
from django.utils.html import mark_safe
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from election.tests import test_adjusted_votes_formula
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
            ('voting_exception', 'Can vote in election even if the user does not satisfy the voting conditions'),
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
    kisa_in_debate_member_email_list = models.TextField(blank=True)
    adjusted_votes_formula = models.TextField(blank=False, null=True, 
        default='((kivm) / (kiva) + (kovm + nkvm) / (kova + nkva)) * 0.5', 
        help_text='The variables allowed to be used: kiva, kivm, kova, kovm, nkva and nkvm'
    )
    adjusted_votes_explanation = models.TextField(blank=True, null=True)
    
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

    def clean(self):
        adjusted_votes_formula = self.adjusted_votes_formula
        
        formula_test_result = test_adjusted_votes_formula(adjusted_votes_formula)
        if formula_test_result != 'OK':
            raise ValidationError(formula_test_result)
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
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
        self.kisa_member_email_list = self.kisa_member_email_list.strip()
        self.kisa_in_debate_member_email_list = self.kisa_in_debate_member_email_list.strip()
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
    joined_debate = models.BooleanField(default=False, null=True)


@receiver(models.signals.post_save, sender=Election)
def update_election(sender, instance, *args, **kwargs):
    kisa_in_debate_member_email_list = instance.kisa_in_debate_member_email_list.split('\n')
    for in_debate_member_email in kisa_in_debate_member_email_list:
        voters = instance.voters.filter(joined_debate=False, user__kaist_email=in_debate_member_email)
        for voter in voters:
            voter.joined_debate = True
            voter.save(update_fields=['joined_debate'])
    
    kisa_member_email_list = instance.kisa_member_email_list.split('\n')
    for kisa_member_email in kisa_member_email_list:
        voters = instance.voters.filter(is_kisa=False, user__kaist_email=kisa_member_email)
        for voter in voters:
            voter.is_kisa = True
            voter.save(update_fields=['is_kisa'])

    voters_kisa_in_debate = instance.voters.filter(joined_debate=True)
    for voter in voters_kisa_in_debate:
        if voter.user.kaist_email not in kisa_in_debate_member_email_list:
            voter.joined_debate = False
            voter.save(update_fields=['joined_debate'])
    
    voters_kisa = instance.voters.filter(is_kisa=True)
    for voter in voters_kisa:
        if voter.user.kaist_email not in kisa_member_email_list:
            voter.is_kisa = False
            voter.save(update_fields=['is_kisa'])

@receiver(models.signals.post_save, sender=Voter)
def update_voter(sender, instance, *args, **kwargs):
    voted_election = instance.voted_election
    kaist_email = instance.user.kaist_email
    if kaist_email is None: 
        assert(instance.user.is_staff) # The opposite case should never happen
        kaist_email = 'kisa@kaist.ac.kr'

    def update_email_list(email_list, email, should_exist):
        if should_exist:
            if email_list.find(email) == -1:
                email_list = f'{email_list.strip()}\n{email}'
        else:
            email_list = email_list.replace(f'{email}\n', '')
            email_list = email_list.replace(f'\n{email}', '')
            email_list = email_list.replace(f'{email}', '')
        return email_list

    voted_election.kisa_member_email_list = \
        update_email_list(voted_election.kisa_member_email_list, kaist_email, instance.is_kisa)
    voted_election.kisa_in_debate_member_email_list = \
        update_email_list(voted_election.kisa_in_debate_member_email_list, kaist_email, instance.joined_debate)

    voted_election.save(update_fields=['kisa_member_email_list', 'kisa_in_debate_member_email_list'])

