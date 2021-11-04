from django.contrib import admin
from adminsortable.admin import SortableAdmin

from .models import MainContent, Member, DivisionDescription, InternalBoardMember

class BaseMemberAdmin(admin.ModelAdmin):
  ordering = ['-year', 'semester', 'position', 'name']

class BaseContentAdmin(SortableAdmin):
  exclude = ['the_order']

class InternalBoardAdmin(SortableAdmin):
  exclude = ['the_order']

admin.site.register(MainContent, BaseContentAdmin)
admin.site.register(DivisionDescription, BaseContentAdmin)
admin.site.register(Member, BaseMemberAdmin)
admin.site.register(InternalBoardMember, InternalBoardAdmin)


# Register your models here.
