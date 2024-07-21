from django.db import models
from core.models import Tag, TagFilterManager

# Create your models here
class MultimediaImage(models.Model):
    """
        IMAGE CLASS TO KEEP IMAGES, TITLE, ALT FOR SEO AND THE IMAGE FILEPATH. 
        ADDITIONAL FEATURES : 
    """
    alt     = models.CharField(max_length = 100,help_text="Enables screen readers to read the information about the image")
    file    = models.ImageField(upload_to = 'images')
    date    = models.DateField()

    def __str__(self):
        return self.file.path


class Multimedia(models.Model):
    """
        THE MODEL IS USED TO COLLAGE MANY IMAGES INTO ONE BIG SET WITH A GIVEN TITLE.
        ANY OTHER MODEL CAN USE THIS MODEL TO ACCESS PICTURES STORED IN THE DATABASE.
    """
    title = models.CharField(max_length = 100)
    slug  = models.SlugField(unique = True)
    images = models.ManyToManyField(MultimediaImage, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.title
