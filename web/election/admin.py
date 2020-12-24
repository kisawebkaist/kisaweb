from django import forms
from django.contrib import admin
from django.utils.html import mark_safe

from .models import Candidate, Election

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
    ]

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

    readonly_fields = ['image_tag']


class ElectionAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'candidates_list',
    ]

    def candidates_list(self, obj):
        return mark_safe('<br />'.join([c.name for c in obj.candidates.all()]))


class VoterAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_email', 'voted_candidate', 'vote_type', 'is_kisa', 'user_status']
    search_fields = ['user__email']
    list_filter = ['is_kisa', 'user__is_staff', 'voted_candidate']
    readonly_fields = ['voted_candidate', 'user', 'vote_type']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def user_email(self, x):
        return x.user.email

    def user_status(self, x):
        return x.user.is_staff


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Election, ElectionAdmin)
