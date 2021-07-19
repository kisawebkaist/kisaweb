from django.db import models
from django.utils.html import mark_safe
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify

from tinymce.models import HTMLField

from web.settings import BASE_DIR


# Create your models here.
CATEGORY = (
    ("", "---"),
    ("Student life", "Student"),
    ("Academics", "Academics"),
    ("Advices", "Advices"),
    ("nothing", "nothing"),
)

'''
class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE, choices = CATEGORY)

    class Meta:
        unique_together = ('slug', 'parent',)
        verbose_name_plural = "categories"

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

'''
'''
class Category(models.Model):
   name = models.CharField(max_length=255)

   def __str__(self):
       return self.name

   def get_absolute_url(self): #url name
       # return reverse('article-detail', args=(str(self.id)))
       return reverse('home')
'''
class Category(models.Model):
   title_category = models.CharField( max_length= 200 , blank=True, choices = CATEGORY )

class Question(models.Model):
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    faq = models.BooleanField()
    '''
    category = models.CharField(
        max_length=20,
        choices=CATEGORY,
        default='nothing'
    )
    '''
    category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.CASCADE, choices=CATEGORY)
    faq_answer = models.TextField(null=True, blank=True)


class Answer(models.Model):
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

