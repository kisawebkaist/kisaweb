from django.db import models
from django.conf import settings
from django.utils.html import mark_safe
from django.dispatch import receiver


class Image(models.Model):
    """
        IMAGE CLASS TO KEEP IMAGES, TITLE, ALT FOR SEO AND THE IMAGE FILEPATH. 
        ADDITIONAL FEATURES : 
    """
    title   = models.CharField(max_length = 100)
    alt     = models.CharField(max_length = 100,help_text="Enables screen readers to read the information about the image")
    date    = models.DateField()
    user    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    user.kaist_email = "testing@kaist.ac.kr"

    file    = models.ImageField(upload_to = f'image_uploader/{user.kaist_email}/images')

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % (self.file.url))

    image_tag.short_description = 'Image'

    def save(self, *args, **kwargs):
        if self.file: 
            self.file.name = f'{self.user.username}_{self.title}_{self.date}.{self.file.name.split(".")[-1]}'
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)


