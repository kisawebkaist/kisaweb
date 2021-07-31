from django.db import models
from tinymce.models import HTMLField

class Main(models.Model):
    title = models.CharField(max_length=2000)
    desc = HTMLField()
    def __str__(self):
        return self.desc

class Members(models.Model):
    title = models.CharField(max_length=2000)
    def __str__(self):
        return self.title

class Division(models.Model):
    title = models.CharField(max_length=2000)
    desc = HTMLField()
    def __str__(self):
        return self.title
