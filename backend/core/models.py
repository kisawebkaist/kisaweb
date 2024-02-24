from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from jsonschema import ValidationError as JSONValidationError
from jsonschema import Draft7Validator

from tinymce.models import HTMLField

# Validators
separator_validator = RegexValidator(r'[^\w\-]', inverse_match=True, message='Spaces and punctuation (except "-" and "_") are not allowed.')

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
    tag_name = models.CharField(max_length=50, blank=False, unique=True, validators=[separator_validator])
    def __str__(self):
        return self.tag_name

    class Meta:
        abstract = True


class Content(models.Model):
    title = models.CharField(max_length=200, blank=False)
    content = HTMLField()
    new_content = models.JSONField(default = dict)
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

class Category(models.Model):
    title_category = models.CharField(max_length= 200, blank=True, unique=True)

    def __str__(self):
        return self.title_category

    def slugified(self):
        """
        Slugify the title of the category for use in id and other cases where spaces and punctuation (except "-" and "_") are not allowed
        """
        return slugify(self.title_category)

    class Meta:
        abstract = True


# End of Abstract Classes


class EmptyQueryset(models.Model):
    events = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        # if you'll not check for self.pk
        # then error will also raised in update of exists model
        if not self.pk and EmptyQueryset.objects.all():
            raise ValidationError('There is can be only one EmptyQueryset instance')
        return super().save(*args, **kwargs)


class Misc(models.Model):
    data = models.JSONField()
    schema = models.JSONField()
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)

    def clean(self):
        try:
            Draft7Validator(self.schema).validate(self.data)
        except JSONValidationError as e:
            ValidationError(params=e.schema, message=e.message)
