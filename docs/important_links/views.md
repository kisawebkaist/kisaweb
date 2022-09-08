# Views

## links_view
This is a list view of all important links


The context will return a list of categories, which will be used to render important links grouped
by category on the frontend.

The following context object will be accessible on the frontend template.
```python
{
    'categories': list, # A list of categories
}
```