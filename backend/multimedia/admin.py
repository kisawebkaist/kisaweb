from django.contrib import admin
import multimedia.models as model
from django.utils.html import format_html
from zipfile import ZipFile, is_zipfile
import os
from io import BytesIO
from datetime import datetime
import PIL
from django.core.files.uploadedfile import SimpleUploadedFile
from django import forms

from core.admin import register, site
from .models import Multimedia, Image

# Register your models here.
site.register(model.Video) # These two are needed to make the Image and Video instances from Multimedia page
site.register(model.Image)

@register(model.MultimediaTag)
class MultimediaTag(admin.ModelAdmin):
  list_display = [
    'tag_name'
  ]

# define a custom form for the multimedia instance, to restrict the set of candidate
# preview or carousel images under the images associated with the current model
class MultimediaAdminForm(forms.ModelForm):
    class Meta:
        model = Multimedia
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(MultimediaAdminForm, self).__init__(*args, **kwargs)
        # if we have an existing instance, then update its querysets for preview and carousels
        # to all the images of that instance
        if self.instance.id:
            self.fields['preview'].queryset = self.instance.images.all()
            self.fields['carousels'].queryset = self.instance.images.all()
        # else, just keep the querysets none
        else:
          self.fields['preview'].queryset = Image.objects.none()
          self.fields['carousels'].queryset = Image.objects.none()

@admin.register(model.Multimedia)
class MultimediaAdmin(admin.ModelAdmin):

  prepopulated_fields = {"slug" : ["title",]}
  readonly_fields = ('current_images',)

  form = MultimediaAdminForm

  # render the current images on the admin panel as a readonly field.
  # supposed to help the users make sense/visualize what kind of images could be a good
  # candidate for preview and carousels
  def current_images(self, obj):
    # Recently added will show up on top
    image_data = '<label>{title}</label><a href="{url}" target="_blank"><img src="{url}" style="width:220px;margin-bottom:3px"/></a>'
    html = ''.join(image_data.format(title=f"[{image.id}] {image.title}", url=image.file.url) for image in obj.images.all().order_by('-pk'))
    return format_html(f'<div style="overflow:scroll;width:240px; height:240px;padding:10px">{html}</div>')

  # this method is used for post-processing the uploaded zip file
  # extracts the images inside the zip file and updates the model content
  def save_related(self, request, form, formsets, change):
    # save the model form straightforwardly
    super(MultimediaAdmin, self).save_related(request, form, formsets, change)
    # retrieve the instance we saved
    instance = form.instance
    # if the instance had a file uploaded
    if instance.multiple_images.name:
        # if the file is a zip file
        if is_zipfile(instance.multiple_images):
            # open that file as a zip file
            with ZipFile(instance.multiple_images) as zip_file:
                # retrieve the names of the contents
                names = zip_file.namelist()
                # per name
                for name in names:
                    # open the corresponding file
                    with zip_file.open(name) as f:
                        # read its data
                        data = f.read()
                        # uses bytesIO to create a file-like object
                        dataEnc = BytesIO(data)
                        # tries the following block, if it succeeds, then it is an image
                        try:
                            # try opening the image file with PIL
                            img = PIL.Image.open(dataEnc)
                            # verify whether the image is broken or not
                            img.verify()
                            # get the current date/time
                            datenow = datetime.now()
                            # make a title for the image (to avoid name collision, integrate the date/time)
                            title = f'{datenow.strftime("%m/%d/%Y, %H:%M:%S")}-{name}'
                            # create a SimpleUploadedFile object which simulates a file uploaded from a form
                            file = SimpleUploadedFile(title, data, content_type='image')
                            # create an image instance
                            instance.images.create(title=title, alt=title, file=file, date=datenow)
                        except:
                            # if there are problems with the file, then skip it
                            pass
        # remove the existing zip file from the server (avoid memory leak)
        os.remove(instance.multiple_images.path)
        # set the multiple_images field to None, since we have already processed it
        instance.multiple_images = None
        # save the instance (but only update the multiple_images field, since we do not need update for m2m fields)
        instance.save(update_fields=['multiple_images'])
  
  current_images.short_description = "All Images of This Multimedia"

