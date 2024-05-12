from django.contrib import admin
from django import forms
from django_draftjs import EditorWidget

from .models import MainContent, Member, DivisionContent, InternalBoardMember, ConstitutionPDF

class BaseContentAdmin(admin.ModelAdmin):
  exclude = ['the_order']

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
  ordering = ['-year', 'semester', 'division', 'name']

@admin.register(InternalBoardMember)
class InternalBoardAdmin(admin.ModelAdmin):
  exclude = ['the_order']

@admin.register(DivisionContent)
class DivisionContentAdmin(admin.ModelAdmin):
  class Form(forms.ModelForm):
    desc = forms.JSONField(widget = EditorWidget())
    class Meta: 
      model = DivisionContent
      fields = [
        'division_name', 
        'desc',
        'image'
      ]
  form = Form

@admin.register(MainContent)
class MainContentAdmin(admin.ModelAdmin):
  class Form(forms.ModelForm):
    desc = forms.JSONField(widget = EditorWidget())
    class Meta: 
      model = MainContent
      fields = [
        'title', 
        'desc',
        'image'
      ]
  form = Form

admin.site.register(ConstitutionPDF)

