from django.db import models
from tinymce.models import HTMLField
from datetime import date
from django.utils import timezone

class MainContent(models.Model):
    title   = models.CharField(max_length = 100, null = True)
    desc    = HTMLField()
    
    def __str__(self):
        return self.title

class BaseMember(models.Model):
    name    = models.CharField(max_length = 100, null = True)
    image   = models.ImageField()
    year    = models.PositiveIntegerField(null=True)
    semester= models.CharField(max_length=10, null=True)
    position= models.CharField(max_length = 100, null = True)

    def save(self, *args, **kwargs):
        cur_date = date.today()
        self.year = cur_date.year
        self.semester = 'Fall' if cur_date.month > 6 else 'Spring'
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'[{self.semester}-{self.year} {self.position}] - {self.name}'

class Member(BaseMember):
    pass

class InternalBoardMember(BaseMember):
    pass
    
class DivisionDescription(models.Model): 
    title   = models.CharField(max_length = 100, null = True)
    desc    = HTMLField()
    
    def __str__(self):
        return self.title
