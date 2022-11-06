from django.db import models
from core.models import Tag, TagFilterManager

# Create your models here


class MultimediaTag(Tag):
    pass


class Video(models.Model):
    """
        VIDEO CLASS ONLY WITH TITLE SLUG AND THE FILEPATH. 
        ADDITIONAL FEATURES :
    """
    title   = models.CharField(max_length = 100)
    url     = models.CharField(max_length=512, blank=False, null=True)
    date    = models.DateField()

    # define the video embedding ratio options
    EMBED_VIDEO_RATIO_CHOICES = [
        ('21by9', '21by9'),
        ('16by9', '16by9'),
        ('4by3', '4by3'),
        ('1by1', '1by1'),
    ]
    embed_video_ratio = models.CharField(max_length=10, default='16by9', choices=EMBED_VIDEO_RATIO_CHOICES)

    def __str__(self):
        return self.title

    # post-process the url information during the saving procedure of the model instance
    # changes 'watch?v=' to 'embed'
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.url: 
            if 'https://www.youtube.com/watch?v=' in self.url:
                self.url = self.url.replace(
                    'https://www.youtube.com/watch?v=',
                    'https://www.youtube.com/embed/'
                )
            if 'https://youtu.be/' in self.url:
                self.url = self.url.replace(
                    'https://youtu.be/',
                    'https://www.youtube.com/embed/'
                )
        super().save(*args, **kwargs)


class Image(models.Model):
    """
        IMAGE CLASS TO KEEP IMAGES, TITLE, ALT FOR SEO AND THE IMAGE FILEPATH. 
        ADDITIONAL FEATURES : 
    """
    title   = models.CharField(max_length = 100)
    alt     = models.CharField(max_length = 100,help_text="Enables screen readers to read the information about the image")
    file    = models.ImageField(upload_to = 'images')
    date    = models.DateField()

    def __str__(self):
        return self.title


class Multimedia(models.Model):
    """
        THE MODEL IS USED TO COLLAGE MANY IMAGES INTO ONE BIG SET WITH A GIVEN TITLE.
        ANY OTHER MODEL CAN USE THIS MODEL TO ACCESS PICTURES STORED IN THE DATABASE.
    """
    title           = models.CharField(max_length = 100)
    slug            = models.SlugField(unique = True)
    date            = models.DateField()
    tags            = models.ManyToManyField(MultimediaTag, blank = True)
    videos          = models.ManyToManyField(Video, blank = True)
    # field for uploading a zip file consisting of multiple images
    multiple_images = models.FileField(blank=True, null=True, help_text="Upload Zip File of Multiple Images") 
    images          = models.ManyToManyField(Image, blank = True)
    # keeps the preview image
    preview         = models.ForeignKey(Image, related_name = "cover_media" ,on_delete = models.CASCADE, blank = True, null = True, help_text="Pick the Preview Image")
    # keeps the carousel images
    carousels       = models.ManyToManyField(Image, related_name="carousel_media", blank=True)
    # whether it is visible over the multimedia page or not
    visible         = models.BooleanField(default=False, null=False)
    objects = TagFilterManager()
    def __str__(self):
        return self.title
