from django.db import models
from core.models import Category

# Create your models here.
class LinkCategory(Category):
	pass

class Link(models.Model):
	title           = models.CharField(max_length=200)
	url             = models.URLField(unique=True)
	description     = models.CharField(max_length=200, blank=True)
	category        = models.ForeignKey(LinkCategory, on_delete=models.CASCADE, related_name='links', related_query_name='link')
	is_english      = models.BooleanField(default=True)
	requires_sso    = models.BooleanField(default=True)
	external_access = models.BooleanField(default=True)

	def __str__(self):
		return f"{self.title}"
	
	class Meta:
		ordering = ('title',)


