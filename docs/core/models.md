# Models

!!! todo "Incomplete"

## Abstract
These models are meant to be inherited and reused whenever needed. 

Should be used in cases where all of the fields of an abstract model can be applied to implement another model (with some additional fields if needed).

### Tag

Generalized Tag model. Tags are designed for Many-to-Many relationships.

#### Fields

| Field | Type | Required | Description| Contraints |
| :---: | ---- | :------: | :--------: | :--------: |
| `tag_name` | Native | :material-check: | The name of the tag | Max length is 50 (characters) and must be unique |


#### Usage
```python
from core.models import Tag

class AppTag(Tag):
	pass
```
Check [custom additions](../core/custom-additions.md) for rendering a tag selection component on the frontend.

### Category

#### Fields

Generalized Category model. Categories are designed for Many-to-One relationships.

| Field | Type | Required | Description| Contraints |
| :---: | ---- | :------: | :--------: | :--------: |
| `title_category` | Native | :material-check: | The title of the category | Only '_' and '-' accepted as separators. Max 200 chars and must be unique |


### Content

Generalized form of a post/content model.

#### Fields

| Field | Type | Required | Description| Contraints |
| :---: | ---- | :------: | :--------: | :--------: |
| `title` | Native | :material-check: | The title of the Content | Max length of 200 (characters) |
| `content` | Native | :material-check: | This is an HTMLField which renders a text field as a TinyMCE editor |  |
| `created` | Native |  | Creation date | Automatically set at creation. Does not change upon edits |
| `modified` | Native |  | Modification date | Automatically set at creation and each update. Changes upon edits |
| `slug` | Native |  | Slug version of title for use in urls | Automatically created from title and creation date |

