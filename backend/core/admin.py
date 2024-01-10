from django.contrib import admin

from .models import User
# from adminsortable.admin import SortableAdmin

# # Register your models here.

# admin.site.site_header = 'KISA Web Administration'

# class DivisionItemAdmin(SortableAdmin):
#   exclue = ['the_order']

# admin.site.register(Footer)
# admin.site.register(Navbar)

admin.site.register(User)