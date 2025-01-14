from django.contrib import admin

from core.admin import register, site
from .models import FAQ
from .models import Category

# Register your models here.

class FAQAdmin(admin.ModelAdmin):
    list_display = ['short_question']

site.register(FAQ, FAQAdmin)
site.register(Category)
