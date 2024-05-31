from django import forms
from django.contrib import admin

from core.admin import register, site
from .models import *

from django_draftjs import EditorWidget

class CandidateForm(forms.ModelForm):
    manifesto = forms.JSONField(widget=EditorWidget())
    kisa_history = forms.JSONField(widget=EditorWidget())
    class Meta:
        model = Candidate
        exclude = [
            'num_votes'
        ]

class ElectionForm(forms.ModelForm):
    intro_msg = forms.JSONField(widget=EditorWidget())
    instructions = forms.JSONField(widget=EditorWidget())
    class Meta:
        model = Election
        fields = '__all__'

@register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'is_open_public']
    form  = CandidateForm
    ordering = ['-election__start_datetime']

    def candidate(self, obj):
        return str(obj)
    
    def has_change_permission(self, request, obj= None):
        return super().has_change_permission(request, obj) #or (obj != None and request.user == obj.account)

@register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ['slug', 'is_open_public', 'results_out', 'results_archived']
    form = ElectionForm

class VoteAdmin(admin.ModelAdmin):
    pass

@register(DebateAttendance)
class DebateAttendanceAdmin(admin.ModelAdmin):
    pass

@register(VotingExceptionToken)
class VotingExceptionTokenAdmin(admin.ModelAdmin):
    pass


# class VoterAdmin(admin.ModelAdmin):
#     list_display = ['user', 'user_email', 'is_kisa', 'joined_debate', 'voted_election']
#     search_fields = ['user__kaist_email', 'user__username']
#     list_filter = ['is_kisa', 'joined_debate']
#     readonly_fields = ['user', 'user_email', 'voted_election']
#     exclude = ['voted_candidate', 'vote_type'] # do not show the vote details in the admin page

#     def get_actions(self, request):
#         actions = super().get_actions(request)
#         if 'delete_selected' in actions:
#             del actions['delete_selected']
#         return actions

#     def has_add_permission(self, request, obj=None): # do not allow adding voters
#         return False

#     def has_delete_permission(self, request, obj=None): # only super user can delete voters
#         if request.user.is_superuser:
#             return True
#         return False

#     def user_email(self, x):
#         return x.user.kaist_email

#     def user_status(self, x):
#         return x.user.is_staff

