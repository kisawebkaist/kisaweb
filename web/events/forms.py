from django import forms
from django.conf import settings
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Submit,
    Row,
    Column,
    Div,
    HTML,
    Field,
    Reset,
    Button,
)
from crispy_forms.bootstrap import (
    UneditableField,
)
from tinymce.widgets import TinyMCE

from .models import Event


# class EventForm(forms.ModelForm):
#     class Meta:
#         model = Event
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_method = 'post'



### Below is a custom made form kept for future reference ###

class EventForm(forms.ModelForm):
    max_occupancy_is_current_occupancy = forms.BooleanField(
        required=False,
        label='Set max occupancy as current occupancy',
    )
    no_registration = forms.BooleanField(
        required=False,
        label='Registration not required',
    )
    
    no_prize = forms.BooleanField(
        required=False,
        label='Event offers prizes',
    )
    
    location = forms.CharField(initial=Event.default_location)
    custom_image_dimensions = forms.BooleanField(required=False)

    class Meta:
        model = Event
        fields = '__all__'
        labels = {
            'max_occupancy': 'Max Occupancy (leave empty if no limit)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if field.widget.__class__ == forms.DateTimeInput:
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += 'datetimepicker'
                else:
                    field.widget.attrs.update({'class': 'datetimepicker'})

        image_id = 'image'
        self.current_image = self.instance.image_tag(css_class='border border-dark rounded', tag_id=image_id)

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('title'),
                Column('location'),  # Check bug fix below
                Column('link'),
            ),
            Row(
                Column(css_class='col-lg-4'),
                Column('is_link', css_class='col-lg-8 col-md'),
            ),
            Row(
                Column('event_start_datetime', css_class='col-lg-3 col-md-6'),
                Column('event_end_datetime', css_class='col-lg-3 col-md-6'),
                Column('registration_start_datetime', css_class='col-lg-3 col-md-6'),
                Column('registration_end_datetime', css_class='col-lg-3 col-md-6'),
            ),
            Row(
                Column(css_class='col-lg-6'),
                Column('no_registration', css_class='col-lg-6 col-md'),
            ),
            Row(
                Column('prize1', css_class='col-lg-3 col-md-6'),
                Column('prize2', css_class='col-lg-3 col-md-6'),
                Column('prize3', css_class='col-lg-3 col-md-6'),
            ),
            Row(
                Column(css_class='col-lg-6'),
                Column('no_prize', css_class='col-lg-6 col-md'),
            ),
            Row(
                Column(
                    'max_occupancy',
                    'max_occupancy_is_current_occupancy',
                    css_class='col-md',
                ),
                Column(
                    UneditableField('current_occupancy'),
                    css_class='col-md',
                ),
            ),
            'important_message',
            'description',
            Field('image', id=image_id),
            'custom_image_dimensions', # 1
            Div(
                Row(
                    Column(UneditableField('image_height')), # 1
                    Column(UneditableField('image_width')), # 1
                ),
                HTML('<button class="btn btn-link py-0" id="image_dim_reset" formnovalidate name="image_dim_reset" style="display: none;">Reset</button>'),
                id='image_contains_info_dimensions',
                css_class='border rounded p-2 mb-3 bg-light',
            ),
            HTML(
                'Current Image<div class="my-2">' + self.current_image + '</div>'
            ),
            Row(
                Column(
                    Submit('submit', 'Save Event', css_class='mr-2'),
                    # Reset('reset', 'Reset Form', css_class='btn btn-secondary mr-2'),
                    Submit('cancel', 'Cancel', formnovalidate='', css_class='btn btn-warning mr-2'),
                ),
                css_class='my-4',
            ),
        )
        # 1. if this name is changed, change is needed in 'image_preview.js'

        # This is a temporary bug fix. "Location" field is "not required" in models.py but crispy forms seems to ignore it somehow.
        self.fields['location'].required = False

    def clean(self):
        try:
            cleaned_data = self.cleaned_data
        except ValidationError:
            return None
        rsd = cleaned_data['registration_start_datetime']
        red = cleaned_data['registration_end_datetime']

        if bool(rsd) ^ bool(red):
            raise ValidationError('Fill both registration datetimes or check the no registration box.', code='incomplete')

        return cleaned_data

    def save(self, commit=True):
        if commit:
            instance = super().save()
        instance.slug = str(instance.pk) + '-' + slugify(instance.title)
        if commit:
            instance.save()
        return instance
