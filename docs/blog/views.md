# Views

## post_view
This is the view for a specific blog post.

!!! note "Query parameter: slug"
	The route to this view will expect a slug passed in as a parameter and it will be used to query the database for a post matching it.

The following context object will be accessible on the frontend template.

```python
{
    'content': str,  # A string of the actual content of the blog post
    'title'  : str,  # A string of the title of the blog post
    'tags'   : list, # A list of tags associated with the blog post
    'image'  : str,  # A string of the path to the image (for use in src attribute)
    'created': str,  # A date string for when the blog post was created
}
```

## blog_view
This is the view for the home page of blog app, with all blogs displayed (with recent posts first).
The tag filtering button can be used to filter for blog posts.

The following context object will be accessible on the frontend template.

```python
{
    'tagObjects'                : list, # A list of all the tags in the database
    'posts'                     : list, # A list of all the posts on the current page (after being filtered for any tags)
	
	# The following are to facilitate the pagination
    'num_results'               : int,  # The total number of posts (after being filtered for any tags)
    'page_ids'                  : list, # A list of the page ids
    'cur_page'                  : int,  # The current page the user is on
    'query_suffix_for_paginator': str,  # A string with all query parameters except page
}
```