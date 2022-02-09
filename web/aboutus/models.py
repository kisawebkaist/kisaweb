from django.db import models
from tinymce.models import HTMLField
from datetime import date
from adminsortable.models import SortableMixin
from django.utils.html import mark_safe

class BaseContent(SortableMixin):

    class Meta:
        ordering = ['the_order']

    title   = models.CharField(max_length = 100, null = True)
    desc    = HTMLField(null=True)
    image   = models.ImageField(null=True, blank=True)
    the_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def __str__(self):
        return self.title

class BaseMember(models.Model):
    name    = models.CharField(max_length = 100, null = True)
    image   = models.ImageField(null=True, blank=True)
    position= models.CharField(max_length = 100, null = True)
    year    = models.PositiveIntegerField(null=True, blank=True)
    semester= models.CharField(max_length=10, null=True, blank=True)

    def save(self, *args, **kwargs):
        cur_date = date.today()
        if self.year == None:
            self.year = cur_date.year
        if self.semester == None:
            self.semester = 'Fall' if cur_date.month > 6 else 'Spring'
        super().save(*args, **kwargs)

    def image_tag(self):
        if not self.image:
            path = '/static/img/candidate-default-dist.png'
        else:
            path = self.image.url
        return mark_safe(f'<img src="{path}" alt="Member Image" class="card-img-top" style="height: 200px; object-fit: cover;" />')

    def __str__(self):
        return f'[{self.semester}-{self.year} {self.position}] - {self.name}'

class Member(BaseMember):
    pass

class InternalBoardMember(BaseMember, SortableMixin):
    class Meta:
        ordering = ['the_order']
    the_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

class MainContent(BaseContent):
    pass

class DivisionDescription(BaseContent): 
    
    def title_lowercase_unspaced(self):
        return '-'.join(self.title.split(' ')).lower()
    
