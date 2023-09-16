from django.contrib import admin

from .models import FAQ
from .models import Category

# Register your models here.

class FAQAdmin(admin.ModelAdmin):
    list_display = ['short_question']

admin.site.register(FAQ, FAQAdmin)
admin.site.register(Category)
