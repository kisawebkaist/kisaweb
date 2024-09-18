from django.db import models
from django.utils.html import mark_safe
# from tinymce.models import HTMLField
from adminsortable.models import SortableMixin
from django.utils.html import mark_safe

from core.utils import DraftJSEditorField

class BaseContent(SortableMixin):

    class Meta:
        ordering = ['the_order']

    title     = models.CharField(max_length = 100, null = True)
    desc      = DraftJSEditorField(default = dict)
    image     = models.ImageField(null=True, blank=True)
    the_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def __str__(self):
        return self.title

class MainContent(BaseContent):
    pass

class ConstitutionPDF(BaseContent):
    image               = None
    desc                = None
    constitution_file   = models.FileField(upload_to = 'constitution', null = True)

class DivisionContent(BaseContent):
    
    division_name = models.CharField(max_length=50, blank=False, null=True)

    def __str__(self):
        return self.division_name

    def title_lowercase_unspaced(self):
        return '-'.join(self.title.split(' ')).lower()


class BaseMember(models.Model):

    SEMESTERS = (
        ('Spring',  'Spring'),
        ('Fall', 'Fall')
    )
    name     = models.CharField(max_length=100, null=True)
    image    = models.ImageField(null=True, blank=True)
    year     = models.PositiveIntegerField(null=True)
    semester = models.CharField(max_length=10, null=True, choices=SEMESTERS)
    sns_link = models.URLField(null=True, blank=True)
    
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

class InternalBoardMember(BaseMember, SortableMixin):
    
    class Meta:
        ordering = ['the_order']

    POSITIONS = (
        ('President', 'President'),
        ('Division Head', 'Division Head'),
        ('Secretary', 'Secretary'),
        ('Deputy Secretary', 'Deputy Secretary')
    )

    position = models.CharField(max_length=100, null=True, choices=POSITIONS)
    the_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    division = models.ForeignKey(DivisionContent, on_delete=models.deletion.PROTECT, null=True, blank=True)

    def __str__(self):
        return f'[{self.semester}-{self.year} {self.division} {self.position}] - {self.name}'

class Member(BaseMember):

    division = models.ForeignKey(DivisionContent, on_delete=models.deletion.PROTECT, null=True, related_name='members', related_query_name='member')
    
    def __str__(self):
        return f'[{self.semester}-{self.year} {self.division}] - {self.name}'