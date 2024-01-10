from django import forms
from django.contrib import admin
from django.utils.html import mark_safe

from .models import Candidate, Election, Voter

# Register your models here.

class CandidateAdminForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = '__all__'
        widgets = {
            'kisa_history': forms.Textarea(attrs={
                'placeholder': 'text',
            }),
        }


class CandidateAdmin(admin.ModelAdmin):
    form = CandidateAdminForm

    list_display = [
        'name',
        'image_tag',
        'kisa_history_template_string',
        'date',
        'votes',
        'yes',
        'no',
    ]

    def votes(self, x):
        return x.voters.count()

    def yes(self, x):
        return x.voters.filter(vote_type='yes').count()
    
    def no(self, x):
        return x.voters.filter(vote_type='no').count()

    def image_tag(self, obj):
        if not obj.image:
            path = '/static/img/candidate-default-dist.png'
        else:
            path = obj.image.url
        return mark_safe(f'<img src="{path}" alt="Candidate Image" width="150" height="150" />')

    image_tag.short_description = 'Current Image'

    def kisa_history_template_string(self, obj):
        history = obj.kisa_history.split('\n')
        return mark_safe('<br />'.join([line for line in history]))

    kisa_history_template_string.short_description = 'Kisa History'

    readonly_fields = ['image_tag', 'date', 'votes', 'yes', 'no']


class ElectionAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'candidates_list',
    ]

    def candidates_list(self, obj):
        return mark_safe('<br />'.join([c.name for c in obj.candidates.all()]))


class VoterAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_email', 'is_kisa', 'joined_debate', 'voted_election']
    search_fields = ['user__kaist_email', 'user__username']
    list_filter = ['is_kisa', 'joined_debate']
    readonly_fields = ['user', 'user_email', 'voted_election']
    exclude = ['voted_candidate', 'vote_type'] # do not show the vote details in the admin page

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request, obj=None): # do not allow adding voters
        return False

    def has_delete_permission(self, request, obj=None): # only super user can delete voters
        if request.user.is_superuser:
            return True
        return False

    def user_email(self, x):
        return x.user.kaist_email

    def user_status(self, x):
        return x.user.is_staff


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Election, ElectionAdmin)
admin.site.register(Voter, VoterAdmin)
