from django.db import models
from core.models import Category

from urllib.parse import urlparse

# Create your models here.
class LinkCategory(Category):
	"""
	Model for link categories

	title_category: title of the link category (inherited field)
	"""
	pass

class Link(models.Model):
	"""
	Model for important links

	title          : Title of the website
	url            : Link of the website
	description    : Short description of the website is used for
	category       : The category under which the link falls
	is_english     : If the website can be natively viewed in english
	requires_sso   : If a KAIST IAM login is required to access the primary functions of the website
	external_access: If the website can be accessed from outside the KAIST campus internet network
	"""
	title           = models.CharField(max_length=200)
	url             = models.URLField(unique=True)
	description     = models.CharField(max_length=200, blank=True)
	category        = models.ForeignKey(LinkCategory, on_delete=models.CASCADE, related_name='links', related_query_name='link')
	is_english      = models.BooleanField(default=True)
	requires_sso    = models.BooleanField(default=True) 
	external_access = models.BooleanField(default=True) 

	def __str__(self):
		return f"{self.title}"
	
	def get_parsed_url(self):
		"""
		str -> ParseResult
		ParseResult(schema, netloc, path, params, query, fragment)

		scheme://netloc/path;parameters?query#fragment

		https://www.example.com/some/page?some_key=some_value
		schema: 'https'
		netloc: 'www.example.com'
		path  : '/some/page'
		query : 'some_key=some_value'
		"""
		return urlparse(self.url)

	class Meta:
		ordering = ('title',)
	


