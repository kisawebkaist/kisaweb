from django.db import models

class UrlShortener(models.Model):
    name    = models.CharField(
        max_length = 50,
        unique = True,
        blank = False,
        null = False
    )
    target  = models.URLField(
        blank = False, null = False
    )

    def __str__(self):
        return self.name
