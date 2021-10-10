# Models

!!! todo "Incomplete"

Both models have been designed with blog Post and PostTag creation from admin panel in mind.

## PostTag

*Inherits [Tag](../core/models.md#tag) from `core`*

Each Post is related to one or more PostTag instances and are used as a way to query for Posts.

### Fields

#### Inherited from Content

* `tag_name`

### Usage
```python	
from blog.models import PostTag

# Two ways to create new Tag
PostTag.objects.create(tag_name="Example")
# or
post_tag = PostTag(tag_name="Example")
post_tag.save()
```

## Post

*Inherits [Content](../core/models.md#content) from `core`*

### Fields

#### Inherited from Content

* `title`
* `content`
* `created`
* `modified`
* `slug`

#### Native

* `tags`: All the tags the Post is associated with.
* `image`: The cover image for the blog Post
	- Constraints:
		- **Optional**
		- Cover image will be resized to 375x375