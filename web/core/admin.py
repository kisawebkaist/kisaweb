from django.contrib import admin

from .models import CourseResources, Footer, CourseUrl

# Register your models here.

admin.site.site_header = 'KISA Web Administration'

class CourseResourceAdmin(admin.ModelAdmin):
    list_display = ['class_id', 'get_url']

    def get_url(self, obj):
        return '\n'.join([url.class_id for url in obj.url.all()])


admin.site.register(CourseResources, CourseResourceAdmin)
admin.site.register(CourseUrl)
admin.site.register(Footer)
