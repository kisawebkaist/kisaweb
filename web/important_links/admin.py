from django.contrib import admin

from .models import Link, LinkCategory
# Register your models here.

admin.site.register(Link)
admin.site.register(LinkCategory)