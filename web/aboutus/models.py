from django.db import models


class Text(models.Model):
    char_text = models.CharField(max_length=2000)
    def __str__(self):
        return self.char_text

class Title(models.Model):
    title_text = models.CharField(max_length=2000)
    def __str__(self):
        return self.title_text
