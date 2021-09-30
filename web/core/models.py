from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from phone_field import PhoneField
from tinymce.models import HTMLField
from django.core.validators import RegexValidator

# Validators
tag_validator = RegexValidator(r'[^\w\-]', inverse_match=True, message='Spaces and punctuation (except "-" and "_") are not allowed.')

# Custom Managers
class TagFilterManager(models.Manager):
    """
    Addon Manager for easy tag based querying on content

    Usage:
    / models.py
        class Example(models.Model):
            objects = TagFilterManager()
            
    
    / Querying
        > tag_list = ['tag1', 'tag2', 'tag3']
        > Example.objects.filter_and(tag_list)
        > Example.objects.filter_or(tag_list)
    """
    def filter_and(self, tag_list):
        """
        AND Operation
        Query for content containing ALL the tags in tag_list.
        If tag_list is equal to [''], all content (without filtering) will be returned
        """
        if tag_list == ['']:
            return self.all()
        return self.filter(tags__tag_name__in=tag_list).annotate(num_tags=models.Count('tags')).filter(num_tags=len(tag_list))
    
    def filter_or(self, tag_list):
        """
        OR Operation
        Query for content containing ANY of the tags in tag_list.
        If tag_list is equal to [''], all content (without filtering) will be returned
        """
        if tag_list == ['']:
            return self.all()
        return self.filter(tags__tag_name__in=tag_list)
    

# End of Custom Managers

# Abstract Classes
class Tag(models.Model):

    tag_name = models.CharField(max_length=50, blank=False, unique=True, validators=[tag_validator])
    def __str__(self):
        return self.tag_name

    class Meta:
        abstract = True


class Content(models.Model):
    title = models.CharField(max_length=200, blank=False)
    content = HTMLField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=100, null=True, unique=True, editable=False)

    def save(self, *args, **kwargs):

        # Saving must occur for the datetime fields to be set automatically, so set it manually if it doesn't exist
        if self.created is None:
            self.created = timezone.now()

        datetime_stamp = self.created.strftime('%Y-%m-%d')
        self.slug = f'{slugify(self.title)}-{datetime_stamp}'

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.slug

    class Meta:
        abstract = True


# End of Abstract Classes


class Footer(models.Model):
    kisa_text = models.CharField(max_length=500, blank=True)

    location = models.CharField(max_length=80, blank=False)
    phnum_eng = PhoneField(blank=False)
    phnum_kor = PhoneField(blank=False)
    email = models.EmailField(max_length=20, blank=False)

    fb_link = models.URLField(blank=True)
    insta_link = models.URLField(blank=True)
    yt_link = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        # if you'll not check for self.pk
        # then error will also raised in update of exists model
        if not self.pk and Footer.objects.all():
            raise ValidationError('There is can be only one Footer instance')
        return super().save(*args, **kwargs)


class EmptyQueryset(models.Model):
    events = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        # if you'll not check for self.pk
        # then error will also raised in update of exists model
        if not self.pk and EmptyQueryset.objects.all():
            raise ValidationError('There is can be only one EmptyQueryset instance')
        return super().save(*args, **kwargs)


class Navbar(models.Model):
    kisa_voice_link = models.URLField(blank=True)
    kisa_books_link = models.URLField(blank=True)
    internships_link = models.URLField(blank=True)
    kaist_ara_link = models.URLField(blank=True)
    course_resources_link = models.URLField(blank=True)
