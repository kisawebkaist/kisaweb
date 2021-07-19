from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.utils.text import slugify
from django.core.validators import RegexValidator
from django.urls import reverse
from django.utils.html import mark_safe 
from PIL import Image
from core.models import Content, Tag

class PostTag(Tag):
  pass

class Post(Content):
  tags = models.ManyToManyField(PostTag)
  default_preview_size = 375 # Testing larger images for design
  image = models.ImageField(upload_to='blog/img', blank=True, null=True)

  def save(self, *args, **kwargs):
    
    # Before returning the save result, create a preview image
    save_result = super(Post, self).save(*args, **kwargs)

    if self.image.name == '' or self.image.name == None: #it means either the file is erased or not added
      return save_result

    # Creates a cropped preview image and stores in the media/blog/img directory 
    self.create_thumbnail_image(self.image.path)

    return save_result

  def get_absolute_url(self):
    return reverse('post', kwargs={'post_slug': self.slug})

  def create_thumbnail_image(self, image_path):
    
    # Open the image with PIL
    saved_image = Image.open(image_path)
    saved_image.thumbnail((self.default_preview_size, self.default_preview_size), Image.ANTIALIAS)
    # Re-format the path-name of the preview image
    path = self.get_preview_format(self.image.path)

    # Save the cropped image
    saved_image.save(path)

    return path

  def get_preview_format(self, path):

    # Simply insert '_pre' before the extension
    pos_dot = path.rfind('.')
    return path[:pos_dot] + '_pre' + path[pos_dot:]

  '''
    This function is used for rendering the image preview on 
    HTML document. It basically returns an image tag with the
    corresponding properties.
  '''
  def get_image_tag(self, css_class='', tag_id=None, pre=True):
    if css_class == '':
      css_class = 'pre-image'

    tag_id_str = ''
    if tag_id:
      tag_id = tag_id + '_preview'
      tag_id_str = f'id="{tag_id}"'
    
    style = ''
    if 'form-image' in css_class:
      style += 'max-width:100%;'
      style += 'height: auto;'  
      if not self.image:
        path = ''
      else:
        path = self.image.url
    else:
      path = self.get_image_path(pre)  
      
    return mark_safe(f'<img src="{path}" class="{css_class}" {tag_id_str} alt="No Image" style="{style}"/>')

  def get_image_path(self, pre):
    if pre:
      return self.get_preview_format(self.image.url)
    return self.image.url