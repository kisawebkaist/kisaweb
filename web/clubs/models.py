from ast import mod
from pyexpat import model
from unicodedata import name
from tinymce.models import HTMLField
from random import choice, choices
from statistics import mode
from django.db import models

# A club class for the following fields
    # Club name
    # Address (contact email)
    # Slogan 
    # Club image
    # Category
    # Description field

class Club(models.Model):
    name = models.CharField(max_length=200, default='Club name')
    slug = models.SlugField(max_length=100, blank=True, editable=False, auto_created=True)
    email = models.EmailField(max_length=50)
    slogan = models.CharField(max_length=500, default='Make KAIST a fun and interesting place to study')
    image = models.ImageField()

    ACADEMIC = 'Academic'
    SPORTS = 'Sports'
    MUSIC = 'Music'
    ARTS = 'Arts'
    LIFE_AND_CULTURE = 'Life and Culture'
    RELIGION_AND_CULTURE = 'Religion and Society'

    choices = [
        (ACADEMIC,'Academic'),
        (SPORTS, 'Sports'),
        (MUSIC, 'Music'),
        (ARTS, 'Arts'),
        (LIFE_AND_CULTURE, 'Life and Culture'),
        (RELIGION_AND_CULTURE, 'Religion and Society')
    ]
    catagory = models.CharField(max_length=50, choices = choices, default= ACADEMIC)
    information = HTMLField()

    def __str__(self) -> str:
        return self.name

        