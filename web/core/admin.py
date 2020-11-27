from django.contrib import admin

from .models import CourseResources

# Register your models here.

admin.site.site_header = 'KISA Web Administration'

admin.site.register(CourseResources)
