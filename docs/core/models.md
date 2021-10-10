# Models

!!! todo "Incomplete"

## Abstract
These models are meant to be inherited and reused whenever needed. 

Should be used in cases where all of the fields of an abstract model can be applied to implement another model.

### Tag

Generalized Tag model.

#### Fields

* `tag_name`: The name of the tag.
	- Constraints:
		- **Required**
		- Max length is 50 (characters).
		- Must be unique.
		

### Usage
```python
from core.models import Tag

class AppTag(Tag):
	pass
```
Check [custom additions](../core/custom-additions.md) for rendering a tag selection component on the frontend.

### Content

Generalized form of a post/content model.

* `title`: The title of the Content.
	- Constraints:
		- **Required**
		- Max length of 200 (characters).
* `content`: The body of the Content.
	- This is an HTMLField which renders a text field as a TinyMCE editor.
* `created`: Creation date.
	- Constraints:
		- Automatically set at creation. Does not change upon edits.
* `modified`: Modification date.
	- Constraints:
		- Automatically set at creation and each update. Changes upon edits.
* `slug`: Slug version of title for use in urls.
	- Constraints:
		- Max length of 100 (characters).
		- Automatically created from title and creation date.

