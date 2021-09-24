from django.db import models
from core.models import Tag

# Create your models here


class MultimediaTag(Tag):
    pass


class Video(models.Model):
    """
        VIDEO CLASS ONLY WITH TITLE SLUG AND THE FILEPATH. 
        ADDITIONAL FEATURES :
    """
    title   = models.CharField(max_length = 100)
    #slug    = models.SlugField(unique   = True)
    file    = models.FileField(upload_to = 'videos')
    date    = models.DateField()

    def __str__(self):
        return self.title


class Image(models.Model):
    """
        IMAGE CLASS TO KEEP IMAGES, TITLE, ALT FOR SEO AND THE IMAGE FILEPATH. 
        ADDITIONAL FEATURES : 
    """
    title   = models.CharField(max_length = 100)
    alt     = models.CharField(max_length = 100)
    #slug    = models.SlugField(unique = True)
    file    = models.ImageField(upload_to = 'images')
    date    = models.DateField()

    def __str__(self):
        return self.title


class Multimedia(models.Model):
    """
        THE MODEL IS USED TO COLLAGE MANY IMAGES INTO ONE BIG SET WITH A GIVEN TITLE.
        ANY OTHER MODEL CAN USE THIS MODEL TO ACCESS PICTURES STORED IN THE DATABASE.
    """
    title    = models.CharField(max_length = 100)
    slug     = models.SlugField(unique = True)
    tags     = models.ManyToManyField(MultimediaTag, blank = True)
    images   = models.ManyToManyField(Image, blank = True)
    videos   = models.ManyToManyField(Video, blank = True)
    date     = models.DateField()
    previews = models.ForeignKey(Image, related_name = "cover_media" ,on_delete = models.CASCADE, blank = True, null = True)

    def __str__(self):
        return self.title
