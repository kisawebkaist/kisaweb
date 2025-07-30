from django.contrib import admin
from web.admin import admin_site
from .models import KISA_Position, Alumni

@admin.register(KISA_Position, site=admin_site)
class KISA_PositionAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Alumni, site=admin_site)
class AlumniAdmin(admin.ModelAdmin):
    list_display = ['name', 'joined_season', 'joined_year', 'separated_season', 'separated_year', 'head_year']
    list_filter = ['joined_year', 'joined_season', 'separated_year', 'separated_season']
    search_fields = ['name']
    filter_horizontal = ['worked_positions']
    readonly_fields = ['work_period']  # Optional if you want to show calculated field
    fieldsets = (
        (None, {
            'fields': ('name', 'picture', 'division', 'head_year')
        }),
        ('Work Period', {
            'fields': ('joined_season', 'joined_year', 'separated_season', 'separated_year', 'worked_positions', 'work_period')
        }),
        ('Contact Info', {
            'fields': ('current_contact',)
        }),
    )

    def work_period(self, obj):
        return obj.work_period
    work_period.short_description = 'Work Period'
