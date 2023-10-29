from typing import Any
from django.db import models

class NavLinkData(models.Model):
    """
    This table contains actual NavLink data.
    """
    href = models.CharField(max_length=100)
    text = models.CharField(max_length=100)
    style = models.TextField()

class NavDropdownData(models.Model):
    """
    This table contains actual NavDropdown data
    """
    display = models.CharField(max_length=100)
    entries = models.ManyToManyField(NavLinkData, through='NavDropdownEntry')

class NavDropdownEntry(models.Model):
    """
    This table is for associating NavLinkData to NavDropdownData
    """
    link = models.ForeignKey(NavLinkData, on_delete=models.CASCADE)
    owner = models.ForeignKey(NavDropdownData, on_delete=models.CASCADE)
    index = models.PositiveIntegerField(unique=True, default=0)

class NavBarEntry(models.Model):
    """
    This table is the index table for navbar entries.
    Each type of data will be represented by an inner class whose table contains two properties;
    - data
    - index

    Both fields are implemented as foreign keys to actual data.
    Addition to those two, there will be
    - type
    which represents the type string
    """
    index = models.PositiveIntegerField(primary_key=True)

    class NavBarLink(models.Model):
        data = models.ForeignKey(NavLinkData, on_delete=models.CASCADE)
        index = models.ForeignKey('NavBarEntry', on_delete=models.CASCADE)
        type = 'link'

    class NavBarDropdown(models.Model):
        data = models.ForeignKey(NavDropdownData, on_delete=models.CASCADE)
        index = models.ForeignKey('NavBarEntry', on_delete=models.CASCADE)
        type = 'dropdown'

    tables = [
        NavBarLink,
        NavBarDropdown
    ]


    def init_custom_fields(self):
        entry = None
        for table in NavBarEntry.tables:
            query = table.objects.filter(index=self.index)
            if query.count() != 0:
                entry = query[0]
                break
        if entry == None:
            raise Exception("Entry not found. Database might be corrupted.")

        self.data = entry.data
        self.type = entry.type

# Added by JOWI
# NOTE: ZWE You can uncomment this part of the code.
# NOTE: This will create a database entry that store only json
# class JSONStorage(models.Model):
#     json = models.JSONField(default = dict) # Fix upload directory
#     name = models.CharField(max_length = 50, default = '') # The name of the particular JSON Store.
#     slug = models.CharField(max_length = 50, default = '')
#     # validator = models.FileField(upload_to = '') or validator = models.JSONField(default = dict)
#     def validate(self):
#         # Do something to validate the JSON
#         pass
