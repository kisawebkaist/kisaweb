from django.contrib import admin
from django import forms
from django_draftjs import EditorWidget

from web.admin import register, admin_site
from .models import *

admin_site.register(KISAMember)

@register(KISARole)
class KISARoleAdmin(admin.ModelAdmin):
  exclude = ['-semester', '-division', '-is_head']

@register(KISADivisionContent)
class DivisionContentAdmin(admin.ModelAdmin):
  class Form(forms.ModelForm):
    content = forms.JSONField(widget = EditorWidget())
    class Meta: 
      model = KISADivisionContent
      fields = '__all__'
  form = Form

