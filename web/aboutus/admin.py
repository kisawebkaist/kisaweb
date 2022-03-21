from django.contrib import admin
from adminsortable.admin import SortableAdmin

from .models import MainContent, Member, DivisionContent, InternalBoardMember

class BaseContentAdmin(SortableAdmin):
  exclude = ['the_order']

class MemberAdmin(admin.ModelAdmin):
  ordering = ['-year', 'semester', 'division', 'name']

class InternalBoardAdmin(SortableAdmin):
  exclude = ['the_order']

admin.site.register(MainContent, BaseContentAdmin)
admin.site.register(DivisionContent, BaseContentAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(InternalBoardMember, InternalBoardAdmin)


# Register your models here.
