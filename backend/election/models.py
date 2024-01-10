from django.db import models
from django.conf import settings
from django.utils.html import mark_safe
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from election.tests import test_adjusted_votes_formula
from tinymce.models import HTMLField

from sso.models import KAISTProfile

# Create your models here.

ELECTION_MEDIA_UPLOAD_URL = 'election/img'

class Candidate(models.Model):
    name = models.CharField(max_length=100, default='') # name of the candidate
    manifesto = HTMLField() # manifesto of the candidate
    speech_url = models.CharField(max_length=512, blank=True, null=True) # url of the candidate's speech video
    kisa_history = HTMLField() # candidate's kisa history
    image = models.ImageField(upload_to=ELECTION_MEDIA_UPLOAD_URL, blank=True, null=True) # candidate's image
    date = models.DateField(auto_now_add=True, null=True) # date the candidate was added to the database

    EMBED_VIDEO_RATIO_CHOICES = [
        ('21by9', '21by9'),
        ('16by9', '16by9'),
        ('4by3', '4by3'),
        ('1by1', '1by1'),
    ] # the candidate video embedding ratio options
    embed_video_ratio = models.CharField(max_length=10, default='16by9', choices=EMBED_VIDEO_RATIO_CHOICES) # the embed video ratio

    def __str__(self):
        return self.name

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

    def change_embed_ratio(self, ratio):
        # update the embed video ratio
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
        ] # some additional permissions for the users regarding the election
    
    start_datetime = models.DateTimeField() # when the election starts
    end_datetime = models.DateTimeField() # when the election ends
    candidates = models.ManyToManyField(Candidate, blank=False) # the election candidates
    intro_msg = HTMLField() # introduction message
    instructions = HTMLField() # election instructions
    image = models.ImageField(upload_to=ELECTION_MEDIA_UPLOAD_URL, blank=True, null=True) # election representative image
    debate_url = models.CharField(max_length=512, blank=True, null=True) # url of the debate video
    is_open_public = models.BooleanField(default=False, null=True) # is the election visible to the public
    results_out = models.BooleanField(default=False, null=True) # are the results visible to the public

    kisa_member_email_list = models.TextField(blank=True, null=True) # emails of the kisa members (to distinguish voting)
    kisa_in_debate_member_email_list = models.TextField(blank=True, null=True) # emails of kisa members who were in the debate (to distinguish voting)
    adjusted_votes_formula = models.TextField(blank=False, null=True, 
        default='((kivm) / (kiva) + (kovm + nkvm) / (kova + nkva)) * 0.5', 
        help_text='The variables allowed to be used: kiva, kivm, kova, kovm, nkva and nkvm'
    ) # the formula used to calculate the adjusted votes
    # accounts for the contribution of the kisa (in/out of debate) members, general votes etc.
    adjusted_votes_explanation = models.TextField(blank=True, null=True) # the explanation of how the adjusted votes are calculated
    
    EMBED_VIDEO_RATIO_CHOICES = [
        ('21by9', '21by9'),
        ('16by9', '16by9'),
        ('4by3', '4by3'),
        ('1by1', '1by1'),
    ] # the candidate video embedding ratio options
    embed_video_ratio = models.CharField(max_length=10, default='16by9', choices=EMBED_VIDEO_RATIO_CHOICES) # the embed video ratio

    def __str__(self):
        month = int(self.start_datetime.strftime('%m'))
        year = self.start_datetime.strftime('%Y')
        if month < 8:
            semester = 'Spring'
        else:
            semester = 'Fall'
        return f'{semester} {year}'

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

    def change_embed_ratio(self, ratio):
        # update the embed video ratio
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
    user = models.ForeignKey(KAISTProfile, on_delete=models.CASCADE, related_name='votes') # the user who votes
    voted_candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='voters') # the candidate who is voted
    voted_election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='voters') # the election in which the vote is casted
    vote_type = models.CharField(max_length=10, blank=True) # the type of the vote (yes/no etc.)
    is_kisa = models.BooleanField(default=False) # is the voter a kisa member
    joined_debate = models.BooleanField(default=False, null=True) # did the voter join the debate


'''
    When an election model instance is updated, the "update_election" signal is sent.
'''

@receiver(models.signals.post_save, sender=Election)
def update_election(sender, instance, *args, **kwargs):

    # if there are voters marked as not joined the debate, but they are in the debate email list
    # then, update their "joined_debate" field to True
    kisa_in_debate_member_email_list = [s.strip() for s in instance.kisa_in_debate_member_email_list.splitlines()]
    for in_debate_member_email in kisa_in_debate_member_email_list:
        voters = instance.voters.filter(joined_debate=False, user__kaist_email=in_debate_member_email)
        for voter in voters:
            voter.joined_debate = True
            voter.save(update_fields=['joined_debate'])
    
    # if there are voters marked as not kisa members, but they are in the kisa email list
    # then, update their "is_kisa" field to True
    kisa_member_email_list = [s.strip() for s in instance.kisa_member_email_list.splitlines()]
    for kisa_member_email in kisa_member_email_list:
        voters = instance.voters.filter(is_kisa=False, user__kaist_email=kisa_member_email)
        for voter in voters:
            voter.is_kisa = True
            voter.save(update_fields=['is_kisa'])

    # if there are voters marked as joined the debate, but they are not in the debate email list
    # then, update their "joined_debate" field to False
    voters_kisa_in_debate = instance.voters.filter(joined_debate=True)
    for voter in voters_kisa_in_debate:
        if voter.user.kaist_email not in kisa_in_debate_member_email_list:
            voter.joined_debate = False
            voter.save(update_fields=['joined_debate'])
    
    # if there are voters marked as kisa members, but they are not in the kisa email list
    # then, update their "is_kisa" field to False
    voters_kisa = instance.voters.filter(is_kisa=True)
    for voter in voters_kisa:
        if voter.user.kaist_email not in kisa_member_email_list:
            voter.is_kisa = False
            voter.save(update_fields=['is_kisa'])

'''

    When a Voter model instance is updated, the "update_voter" signal is sent.

'''

@receiver(models.signals.post_save, sender=Voter)
def update_voter(sender, instance, *args, **kwargs):
    
    voted_election = instance.voted_election
    kaist_email = instance.user.kaist_email
    
    if kaist_email is None: 
        assert(instance.user.is_staff) # The user has to be staff if the kaist_email is None
        kaist_email = 'kisa@kaist.ac.kr'

    # updates an email list (either kisa member or kisa in debate member email list)
    def update_email_list(email_list_str, email, should_exist):
        email_list = [s.strip() for s in email_list_str.splitlines()]
        if should_exist: # if the voter email should exist in the email list
            if not email in email_list: # if the voter email is not in the email list
                # then add the voter email to the email list
                email_list.append(email)
        else: # if the voter email should not exist in the email list
            # then remove the voter email from the email list
            email_list = [e for e in email_list if e != email]
        email_list_str_final = '\n'.join(email_list)

        return email_list_str_final

    # update the email lists based on the update in the voter instance
    voted_election.kisa_member_email_list = \
        update_email_list(voted_election.kisa_member_email_list, kaist_email, instance.is_kisa)
    voted_election.kisa_in_debate_member_email_list = \
        update_email_list(voted_election.kisa_in_debate_member_email_list, kaist_email, instance.joined_debate)

    # save the updated email lists in the corresponding election instance
    voted_election.save(update_fields=['kisa_member_email_list', 'kisa_in_debate_member_email_list'])

