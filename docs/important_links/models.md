# Models

Both models have been designed with blog Link and LinkCategory creation from admin panel in mind.
This means there is no front-end on the website to creat a new important link.

## LinkCategory

*Inherits [Tag](../core/models.md#category) from `core`*

Each Link is related to one LinkCategory. This is used as a way to query links by category.

### Fields

#### Inherited from Category

```
 title_category 
```

### Usage
```python	
from important_links.models import LinkCategory

# Two ways to create new LinkCategory
LinkCategory.objects.create(title_category="Example")
# or
link_category = LinkCategory(title_category="Example")
link_category.save()
```

## Link

### Fields


| Field | Type | Required | Description| Contraints |
| :---: | :--: | :------: | :--------: | :--------: |
|`title`| Native |  | The display title of the link ||
|`url`| Native |  | The url of the link |  |
|`description`| Native |  | Short description of what the linked website contains |  |
|`category`| Native |  | The category of the link |  |
|`is_english`| Native |  | Is the site in english or not |  |
|`requires_sso`| Native |  | Does the site require KAIST SSO to use |  |
|`external_access`| Native |  | Can the site be accessed from off-campus |  |

