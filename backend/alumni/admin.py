from django.contrib import admin

from core.admin import register
from .models import Alumni,KISA_Position
# Register your models here.
register(KISA_Position)
register(Alumni)