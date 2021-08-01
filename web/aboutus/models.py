from django.db import models
from tinymce.models import HTMLField

class Main(models.Model):
    title   = models.CharField(max_length = 100, null = True)
    desc    = HTMLField()
    
    def __str__(self):
        return self.desc

class Members(models.Model):
    name    = models.CharField(max_length = 100, null = True)
    position= models.CharField(max_length = 100, null = True)

    def __str__(self):
        return self.name

class Board(models.Model):
    name    = models.CharField(max_length = 100, null = True)
    position= models.CharField(max_length = 100, null = True)
    quote   = models.TextField()

    def __str__(self):
        return self.name


class Division(models.Model):
    title   = models.CharField(max_length = 100, null = True)
    desc    = HTMLField()
    
    def __str__(self):
        return self.title
