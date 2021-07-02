from django.contrib import admin
import .models as model

# Register your models here.
admin.site.register(model.Video)
admin.site.register(model.Image)
admin.site.register(model.Multimedia)

@admin.register(model.MultimediaTags)
class MultimediaTags(admin.ModelAdmin):
  list_display = [
    'tag_name'
  ]