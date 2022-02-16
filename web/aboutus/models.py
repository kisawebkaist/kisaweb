from tkinter import CASCADE
from django.db import models
from django.utils.html import mark_safe
from tinymce.models import HTMLField
from datetime import date
from adminsortable.models import SortableMixin
from django.utils.html import mark_safe

class BaseContent(SortableMixin):

    class Meta:
        ordering = ['the_order']

    title     = models.CharField(max_length = 100, null = True)
    desc      = HTMLField(null=True)
    image     = models.ImageField(null=True, blank=True)
    the_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def __str__(self):
        return self.title

class BaseMember(models.Model):
    SEMESTERS = (
        ('Spring',  'Spring'),
        ('Fall', 'Fall')
    )
    # POSITIONS = (
    #     ('President', 'President'),
    #     ('Division Head', 'Division Head'),
    #     ('Secretary', 'Secretary'),
    #     ('Member', 'Member')
    # )
    name     = models.CharField(max_length = 100, null = True)
    image    = models.ImageField(null=True, blank=True)
    position = models.CharField(max_length = 100, null = True)
    year     = models.PositiveIntegerField(null=True, blank=True)
    semester = models.CharField(max_length=10, null=True, blank=True, choices=SEMESTERS)
    sns_link = models.URLField(null=True, blank=True)

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
    
    def image_tag(self, css_class='', tag_id=None):
        """
        Creates the HTML image tag with the appropriate image src to show for the member.
        If member image is not provided then aboutus/static/img/anonymous.png is used instead.

        Args:
            css_class (str, default = empty string): Classes to add to the HTML img tag.
            tag_id (str, default = ``None``): ID to add to the HTML img tag.

        Returns:
            str: HTML img tag
        """
        tag_id_str = ''
        if tag_id:
            tag_id = tag_id + '_preview'
            tag_id_str = f'id="{tag_id}"'

        if not self.image:
            path = '/static/img/anonymous.png'
        else:
            path = f'/media/{self.image}'
        return mark_safe(f'<img src="{path}" class="{css_class}" {tag_id_str} alt="Member Image"/>')
    
class MainContent(BaseContent):
    pass

class Division(BaseContent):
    
    def title_lowercase_unspaced(self):
        return '-'.join(self.title.split(' ')).lower()

class InternalBoardMember(BaseMember, SortableMixin):
    class Meta:
        ordering = ['the_order']
    the_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

class Member(BaseMember):
    division = models.ForeignKey(Division, on_delete=models.deletion.CASCADE, null=True, related_name='members', related_query_name='member')
    pass

    
