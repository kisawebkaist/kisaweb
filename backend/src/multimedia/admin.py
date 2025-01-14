from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import transaction
import multimedia.models as model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from zipfile import ZipFile, ZipInfo, is_zipfile
import os
from io import BytesIO
from datetime import datetime
import PIL
from django.core.files.uploadedfile import SimpleUploadedFile
from django import forms
from django.core.validators import FileExtensionValidator, get_available_image_extensions
from PIL import Image

from core.admin import register, site
from .models import *

site.register(model.MultimediaImage)

zip_file_extension_validator = FileExtensionValidator(["zip"])
pil_image_extensions_checkers = [lambda filename, ext=ext: filename.endswith(ext) for ext in get_available_image_extensions()]

def validate_zip_file(value):
    zip_file_extension_validator(value)
    if not is_zipfile(value):
      raise ValidationError(
          _("It is not a zip file")
      )
    if ZipFile(value).testzip() is not None:
        raise ValidationError(
            _("It contains a faulty file")
        )

class MultimediaImageForm(forms.ModelForm):
   class Meta:
      model = MultimediaImage
      fields = '__all__'


# define a custom form for the multimedia instance, to restrict the set of candidate
# preview or carousel images under the images associated with the current model
class MultimediaAdminForm(forms.ModelForm):
    images_zip = forms.FileField(validators=[validate_zip_file], required=False)
    class Meta:
        model = Multimedia
        fields = [
            'title',
            'slug',
            'images',
            'images_zip',
            'description',
        ]

    def clean_images_zip(self):
      images_zip = self.cleaned_data.get("images_zip")
      if images_zip is None:
         return []
      image_files = []
      with ZipFile(images_zip) as zipfile:
        for zipinfo in zipfile.infolist():
          print(zipinfo.filename)
          print(list(map(lambda matches: not matches("hello.png"), iter(pil_image_extensions_checkers))))
          if zipinfo.is_dir() or all(map(lambda matches: not matches(zipinfo.filename), iter(pil_image_extensions_checkers))):
            continue
          print("hello")
          with zipfile.open(zipinfo) as file:
            data = file.read()
            # uses bytesIO to create a file-like object
            dataEnc = BytesIO(data)
            # tries the following block, if it succeeds, then it is an image
            with Image.open(dataEnc) as img:
              # verify whether the image is broken or not
              img.verify()
              # get the current date/time
              datenow = timezone.now()
              # make a title for the image (to avoid name collision, integrate the date/time)
              title = f'{datenow.strftime("%m/%d/%Y, %H:%M:%S")}-{os.path.basename(zipinfo.filename)}'
              # create a SimpleUploadedFile object which simulates a file uploaded from a form
              image_files.append(SimpleUploadedFile(title, data, content_type='image'))
      return image_files
    
    def clean(self):
       cleaned_data = super().clean()
       print(cleaned_data)
       images = []
       with transaction.atomic():
        for image_file in cleaned_data.get("images_zip", []):
            image = MultimediaImage(alt=image_file.name, file=image_file, date=timezone.now())
            image.save()
            images.append(image)
       cleaned_data["images"] = images + list(cleaned_data["images"])
       return cleaned_data

@register(model.Multimedia)
class MultimediaAdmin(admin.ModelAdmin):
  form = MultimediaAdminForm

#   # render the current images on the admin panel as a readonly field.
#   # supposed to help the users make sense/visualize what kind of images could be a good
#   # candidate for preview and carousels
#   def current_images(self, obj):
#     # Recently added will show up on top
#     image_data = '<label>{title}</label><a href="{url}" target="_blank"><img src="{url}" style="width:220px;margin-bottom:3px"/></a>'
#     html = ''.join(image_data.format(title=f"[{image.id}] {image.title}", url=image.file.url) for image in obj.images.all().order_by('-pk'))
#     return format_html(f'<div style="overflow:scroll;width:240px; height:240px;padding:10px">{html}</div>')

#   # this method is used for post-processing the uploaded zip file
#   # extracts the images inside the zip file and updates the model content
#   def save_related(self, request, form, formsets, change):
#     # save the model form straightforwardly
#     super(MultimediaAdmin, self).save_related(request, form, formsets, change)
#     # retrieve the instance we saved
#     instance = form.instance
#     # if the instance had a file uploaded
#     if instance.multiple_images.name:
#         # if the file is a zip file
#         if is_zipfile(instance.multiple_images):
#             # open that file as a zip file
#             with ZipFile(instance.multiple_images) as zip_file:
#                 # retrieve the names of the contents
#                 names = zip_file.namelist()
#                 # per name
#                 for name in names:
#                     # open the corresponding file
#                     with zip_file.open(name) as f:
#                         # read its data
#                         data = f.read()
#                         # uses bytesIO to create a file-like object
#                         dataEnc = BytesIO(data)
#                         # tries the following block, if it succeeds, then it is an image
#                         try:
#                             # try opening the image file with PIL
#                             img = PIL.Image.open(dataEnc)
#                             # verify whether the image is broken or not
#                             img.verify()
#                             # get the current date/time
#                             datenow = datetime.now()
#                             # make a title for the image (to avoid name collision, integrate the date/time)
#                             title = f'{datenow.strftime("%m/%d/%Y, %H:%M:%S")}-{name}'
#                             # create a SimpleUploadedFile object which simulates a file uploaded from a form
#                             file = SimpleUploadedFile(title, data, content_type='image')
#                             # create an image instance
#                             instance.images.create(title=title, alt=title, file=file, date=datenow)
#                         except:
#                             # if there are problems with the file, then skip it
#                             pass
#         # remove the existing zip file from the server (avoid memory leak)
#         os.remove(instance.multiple_images.path)
#         # set the multiple_images field to None, since we have already processed it
#         instance.multiple_images = None
#         # save the instance (but only update the multiple_images field, since we do not need update for m2m fields)
#         instance.save(update_fields=['multiple_images'])
  
#   current_images.short_description = "All Images of This Multimedia"

