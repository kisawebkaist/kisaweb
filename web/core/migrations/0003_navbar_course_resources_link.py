# Generated by Django 3.0 on 2021-08-29 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_navbar'),
    ]

    operations = [
        migrations.AddField(
            model_name='navbar',
            name='course_resources_link',
            field=models.URLField(blank=True),
        ),
    ]