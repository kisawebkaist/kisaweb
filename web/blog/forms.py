from django import forms

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

from .models import Post

'''
  This is a class used for creating a post create/update view.
  It makes our jobs easier to create a form.
'''
class PostForm(forms.ModelForm):

  class Meta:
    model = Post
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    image_id = 'image'
    self.current_image = self.instance.get_image_tag(css_class='form-image', pre=False, tag_id=image_id)
    self.helper = FormHelper(self)
    self.helper.form_method = 'post'

    # This is the layout of the post create/update form page.
    self.helper.layout = Layout(
        Row(
          Column('title'),
          Column('category', 'author'),
        ),
        Row(
          Column('content'),
        ),
        Field('image', id=image_id),
        HTML(
          'Current Image<div class="my-2" style="width:100%">' + self.current_image + '</div>'
        ),
        Row(
          Column(
            Submit('submit', 'Save Post', css_class='mr-2'),
            Reset('reset', 'Reset Form', css_class='btn btn-secondary mr-2'),
            Submit('cancel', 'Cancel', formnovalidate='', css_class='btn btn-warning mr-2'),),
          css_class='my-4',
        ),
      )
  
  def clean(self):
    cleaned_data = self.cleaned_data
    return cleaned_data
  
  def save(self, commit=True):
    if commit:
      instance = super().save()
    instance.slug = instance.get_unique_slug()
    if commit:
      instance.save()
    return instance