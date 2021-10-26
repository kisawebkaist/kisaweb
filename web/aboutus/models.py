from django.db import models
from tinymce.models import HTMLField
from datetime import date
from adminsortable.models import SortableMixin

class BaseContent(SortableMixin):

    class Meta:
        ordering = ['the_order']

    title   = models.CharField(max_length = 100, null = True)
    desc    = HTMLField(null=True)
    the_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

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
    
class MainContent(BaseContent):
    pass

class DivisionDescription(BaseContent): 
    pass
