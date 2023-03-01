from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
# Create your models here.

class Kisa_Position(models.Model):
    name = models.CharField(max_length=255,blank=False,null=False)
    def __str__(self):
        return self.name

class Alumni(models.Model):
    SEASON_CHOICES = [
        ('Spring','Spring'),
        ('Summer','Summer'),
        ('Fall','Fall'),
        ('Winter','Winter')
    ]
    name = models.CharField(max_length=255,blank=False,null=False)
    joined_season = models.CharField(choices=SEASON_CHOICES,max_length=6,default='Spring',blank=False,null=False)
    joined_year = models.IntegerField(default=2004,blank=False,null=False, validators=[MinValueValidator(2004), MaxValueValidator(datetime.date.today().year)])
    separated_season = models.CharField(choices=SEASON_CHOICES, max_length=6,blank=True,null=True,help_text='If the alumni only worked for one season please leave this part empty.')
    separated_year = models.IntegerField(blank=True,null=True, validators=[MinValueValidator(2004), MaxValueValidator(datetime.date.today().year)], help_text='If the alumni only worked for one season please leave this part empty.')
    worked_positions = models.ManyToManyField(Kisa_Position, blank=False)
    current_contact = models.URLField(blank=True,null=True,help_text='Current contact of the Alumni. Be sure to ask the alumni for permission to post it.')
    def __str__(self):
        return self.name