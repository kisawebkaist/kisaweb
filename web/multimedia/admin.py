from django.contrib import admin
import multimedia.models as model

# Register your models here.

@admin.register(model.MultimediaTag)
class MultimediaTag(admin.ModelAdmin):
  list_display = [
    'tag_name'
  ]

@admin.register(model.Multimedia)
class MultimediaAdmin(admin.ModelAdmin):
  prepopulated_fields = {"slug" : ["title",]}