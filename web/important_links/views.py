from django.shortcuts import render, HttpResponse
from .models import Link, LinkCategory

# Create your views here.
def links_view(request):
	categories = LinkCategory.objects.all()
	# Links are accessed from the categories directly

	# LinkCategory.links.all() to access all links in a category
	# Link fields: title, description, url
	# The other link fields (the booleans) can be rendered as small badges perhaps?

	context = {
		'categories': categories
	}
	return render(request, "important_links/links_home.html", context=context)