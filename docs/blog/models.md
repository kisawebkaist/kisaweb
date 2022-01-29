# Models

Both models have been designed with blog Post and PostTag creation from admin panel in mind.
This means there is no front-end on the website to creat a blog post.

## PostTag

*Inherits [Tag](../core/models.md#tag) from `core`*

Each Post is related to one or more PostTag instances and are used as a way to query for Posts.

### Fields

#### Inherited from Content

```
 tag_name
```

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
```python
title, content, created, modified, slug
```
#### Native

| Field | Type | Required | Description| Contraints |
| :---: | :--: | :------: | :--------: | :--------: |
|`tags`| Native | :material-check: | All tags the Post is associtated with ||
|`image`| Native |  | The cover image for the Post | Will be resized to 375x375px |

### Methods

For a `Post` object passed to the front-end titled `blog_post`, use the following in your html file to get the image tag of the blog post's preview image. 

```html
{% if blog_post.image %}
	{{ blog_post.get_image_tag }}
{% endif %}

```

