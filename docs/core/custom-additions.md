# Custom Additions

## Tag Filtering Use

### Backend
Include the following in the context in your `views.py` file:
```python
context = {
	'tagObjects': ExampleTag.objects.order_by('tag_name').all(),
}
```
Replace ExampleTag with the Tag model name in the respective app.

### Frontend
Include the following in your html file:
```html
{% include 'core/tag_filter.html' %}

{% block js %}
<script src="{% static 'js/tag_filter.js' %}"></script>
{% endblock %}
```

### Querying
To query for posts/content based on tags, two things should be done.
```python
# models.py
from core.models import TagFilterManager

class Post(models.Model):
	objects = TagFilterManager()
	...

# views.py
from .models import Post

tag_list = ['tag1', 'tag2', ...]
Post.objects.filter_and(tag_list) # Posts containing all tags in tag_list
Post.objects.filter_or(tag_list) # Posts containing any tag in tag_list
```