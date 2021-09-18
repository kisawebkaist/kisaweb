from django.contrib import admin
import multimedia.models as model

# Register your models here.
admin.site.register(model.Video)
admin.site.register(model.Image)
admin.site.register(model.Multimedia)

@admin.register(model.MultimediaTag)
class MultimediaTag(admin.ModelAdmin):
  list_display = [
    'tag_name'
  ]