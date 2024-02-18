from django import forms
from django.contrib import admin

from .models import *


class CandidateAdmin(admin.ModelAdmin):
    pass

class ElectionAdmin(admin.ModelAdmin):
    pass

class VoteAdmin(admin.ModelAdmin):
    pass

class DebateAttendanceAdmin(admin.ModelAdmin):
    pass

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


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Election, ElectionAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(DebateAttendance, DebateAttendanceAdmin)
admin.site.register(VotingExceptionToken, VotingExceptionTokenAdmin)
