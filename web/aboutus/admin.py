from django.contrib import admin

from .models import MainContent, Member, DivisionDescription, InternalBoardMember

class BaseMemberAdmin(admin.ModelAdmin):
  exclude = ['year', 'semester']
  ordering = ['-year', 'semester', 'position', 'name']

admin.site.register(MainContent)
admin.site.register(DivisionDescription)
admin.site.register(Member, BaseMemberAdmin)
admin.site.register(InternalBoardMember, BaseMemberAdmin)


# Register your models here.
