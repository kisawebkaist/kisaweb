from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

from tinymce.models import HTMLField

from web.settings import BASE_DIR

# Create your models here.

class Event(models.Model):
    """Event(**kwargs)

    .. include:: <isonum.txt>

    Warning:
        If any attribute or method names are changed, change is needed in 'event.forms' and related css and js files.

    Note:
        **The following attributes are database fields.**

    Db_Fields:
        title (CharField)

        slug (SlugField, not user-modifiable):
            Unique name-recognizable identifier for event instance. Cannot be
            modified in UI. Value set to ``{ id }-{ title }`` upon saving the event instance (i.e. changing the title also changes the slug) (see :meth:`Event.save` for code).

        location (CharField, default = :attr:`Event.default_location`)

        event_start_datetime (DateTimeField)
        event_end_datetime (DateTimeField)
        registration_start_datetime (DateTimeField, default = ``None``)
        registration_end_datetime (DateTimeField, default = ``None``)

        max_occupancy (PositiveSmallIntegerField, default = ``None``)
        current_occupancy (PositiveSmallIntegerField, default = ``0``)
        participants (ManyToManyField |rarr| :class:`User`, default = ``None``)
        important_message (CharField, default = ``None``)

        description (tinymce.models.HTMLField)

        descr_truncate_num (PositiveSmallIntegerField, default = :attr:`Event.min_descr_truncate_num`):
            The number of words of description to show in events listview. This is a separate field in the database instead of a value in the HTML file because of the AJAX requests to modify this number.

        image (ImageField, default = event-default-dist.* in events/static/img directory):
            Can include important information (such as a schedule). Dimensions of image file do not have to be something specific, but the dimensions of the image shown in the website can be changed by altering the :attr:`Event.image_height` and :attr:`Event.image_width` fields. Default image is rendered as a square.

        image_height (PositiveSmallIntegerField, default = :attr:`Event.default_image_size`):
            This represents the height of image shown in the website via the HTML :attr:`<img height>` attribute. It is NOT the height of the actual image file.

        image_width (PositiveSmallIntegerField, default = :attr:`Event.default_image_size`):
            This represents the width of image shown in the website via the HTML :attr:`<img width>` attribute. It is NOT the width of the actual image file.

    Note:
        **The following attributes are regular python attributes.**

    Attributes:
        default_location (str)

        min_descr_truncate_num (int):
            The default and minimum number of words required for the description to be truncated.

        default_image_size (int):
            The default HTML width and height of the image.
    """
    title = models.CharField(max_length=100, default='')
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    default_location = 'TBA'
    location = models.CharField(max_length=100, default=default_location)

    event_start_datetime = models.DateTimeField()
    event_end_datetime = models.DateTimeField()
    registration_start_datetime = models.DateTimeField(blank=True, null=True)
    registration_end_datetime = models.DateTimeField(blank=True, null=True)

    max_occupancy = models.PositiveSmallIntegerField(blank=True, null=True)
    current_occupancy = models.PositiveSmallIntegerField(blank=True, default=0)
    participants = models.ManyToManyField(User, blank=True)
    important_message = models.CharField(max_length=200, blank=True)

    description = HTMLField()
    min_descr_truncate_num = 50
    descr_truncate_num = models.PositiveSmallIntegerField(blank=True, default=min_descr_truncate_num)

    default_image_size = 260
    image = models.ImageField(upload_to='events/img', blank=True, null=True)
    image_height = models.PositiveSmallIntegerField(blank=True, default=default_image_size)
    image_width = models.PositiveSmallIntegerField(blank=True, default=default_image_size)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Sets the success url for :mod:`events.views.EventCreate` and :mod:`events.views.EventUpdate`.
        """
        return reverse('event_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        """In addition to the default save method, it saves the :attr:`Event.slug` field of the instance.
        """
        self.slug = str(self.pk) + '-' + slugify(self.title)
        super().save(*args, **kwargs)

    def image_tag(self, css_class='', tag_id=None, listview=False):
        """
        Creates the HTML image tag with the appropriate image src to show for the event instance. This method is implemented since ImageField can not have a default value. If :attr:`Event.image` is ``None``, then the default image stored in 'event/static/img' directory is used.

        Args:
            css_class (str, default = empty string): Classes to add to the HTML img tag.
            tag_id (str, default = ``None``): ID to add to the HTML img tag.
            listview (bool, default = ``False``):
                ``True`` if the image tag will be used in events listview (as opposed to detailview).

        Returns:
            str: HTML img tag
        """
        tag_id_str = ''
        if tag_id:
            tag_id = tag_id + '_preview'
            tag_id_str = f'id="{tag_id}"'

        width, height = self.image_width, self.image_height
        if listview:
            width_height_ratio = width / height
            width = self.default_image_size
            height = width / width_height_ratio

        if not self.image:
            path = '/static/img/events-default-dev-dist.png'
        else:
            path = f'/media/{self.image}'
        return mark_safe(f'<img src="{path}" class="{css_class}" {tag_id_str} alt="Event Image" width="{width}" height="{height}" />')

    def modify_registration(self, registration_type, user):
        """
        Registers or Deregisters a user for an event. The database values for fields :attr:`Event.participants` and :attr:`Event.current_occupancy` are modified.

        Args:
            registration_type (str): Takes the values ``'register'`` or ``'deregister'`` depending on the request.
            user (:class:`User`): User reqesting to be (de)registered.

        Returns:
            str: ``'Full'`` if :attr:`Event.max_occupancy` = :attr:`Event.current_occupancy`.
        """
        if registration_type=='register' and (not self.max_occupancy or self.current_occupancy < self.max_occupancy):
            self.participants.add(user)
            change = 1
        elif registration_type=='deregister' and self.current_occupancy > 0:
            self.participants.remove(user)
            change = -1
        else:
            return 'Full'

        self.current_occupancy = models.F('current_occupancy') + change
        self.save(update_fields=['current_occupancy'])

    def modify_descr_truncate_num(self, num):
        """Modifies the database field value of :attr:`Event.descr_truncate_num`. If the new value is less than :attr:`Event.min_descr_truncate_num`, then the value is set to :attr:`Event.min_descr_truncate_num`.

        Args:
            num (int): The new value for the database field.
        """
        # if the below logic is changed, then change might be needed in 'event_truncation.js'
        self.descr_truncate_num = num if num >= self.min_descr_truncate_num else self.min_descr_truncate_num
        self.save(update_fields=['descr_truncate_num'])
