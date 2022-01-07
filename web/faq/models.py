from django.db import models
from django.template.defaultfilters import truncatechars
from core.models import Category

# Create your models here.
class FAQCategory(Category):
    pass

class FAQ(models.Model):
    question = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name='faqs')
    answer = models.TextField()

    @property
    def short_question(self):
        return truncatechars(f'{self.question}', 150) + f' [{self.category}]'



