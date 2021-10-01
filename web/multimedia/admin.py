from django.contrib import admin
import multimedia.models as model
from django.utils.safestring import mark_safe
from django.utils.html import format_html

# Register your models here.
admin.site.register(model.Video) # These two are needed to make the Image and Video instances from Multimedia page
admin.site.register(model.Image)

@admin.register(model.MultimediaTag)
class MultimediaTag(admin.ModelAdmin):
  list_display = [
    'tag_name'
  ]

@admin.register(model.Multimedia)
class MultimediaAdmin(admin.ModelAdmin):
  prepopulated_fields = {"slug" : ["title",]}

  readonly_fields = ('image_options',)

  def image_options(self, obj):
    # Recently added will show up on top
    image_data = '<label>{title}</label><a href="{url}" target="_blank"><img src="{url}" style="width:220px;height:200px;margin-bottom:3px"/></a>'
    html = ''.join(image_data.format(title=f"[{image.id}] {image.title}", url=image.file.url) for image in model.Image.objects.all().order_by('-pk'))
    return format_html(f'<div style="overflow:scroll;width:240px; height:240px;padding:10px">{html}</div>')

  # The following is for previewing the images already added to the Multimedia object. Only shows up after saving once.
  # def added_images(self, obj):
  #   html = '<a href="{url}" target="_blank"><img src="{url}" style="width:150px;height:150px"/></a>'
  #   # print(obj.images.all())
  #   return format_html(''.join(html.format(url=image.file.url) for image in obj.images.all()))
  
  image_options.short_description = "All Images on Server"

