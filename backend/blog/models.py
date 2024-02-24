from django.db import models
from PIL import Image
from core.models import Content, Tag
import pathlib

class PostTag(Tag):
    pass

class Post(Content):
    tags = models.ManyToManyField(PostTag)
    description = models.CharField(max_length = 255, default = '')
    default_preview_size = 375 # Testing larger images for design
    image = models.ImageField(upload_to='blog/img', blank=True, null=True)

    def image_exists(self):
        return not (self.image.name == '' or self.image.name == None)

    def preview_image_path(self):
        image_path = self.image_path()
        image_name = image_path.stem
        return image_path.parent / f'{image_name}_pre.{image_path.suffix}'

    def image_path(self):
        return pathlib.Path(self.image.path)

    def save(self, *args, **kwargs):
        save_result = super(Post, self).save(*args, **kwargs)
        if self.image_exists():
            self.create_thumbnail_image(self.image.path)
        return save_result

    def create_thumbnail_image(self, image_path : str):
        saved_image = Image.open(image_path)
        saved_image.thumbnail(
            (self.default_preview_size, self.default_preview_size)
        )
        path = self.preview_image_path()
        saved_image.save(path)
