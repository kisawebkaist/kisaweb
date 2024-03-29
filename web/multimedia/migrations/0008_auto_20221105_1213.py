# Generated by Django 3.0 on 2022-11-05 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia', '0007_auto_20221105_1133'),
    ]

    operations = [
        migrations.RenameField(
            model_name='multimedia',
            old_name='previews',
            new_name='preview',
        ),
        migrations.AddField(
            model_name='multimedia',
            name='carousels',
            field=models.ManyToManyField(blank=True, related_name='carousel_media', to='multimedia.Image'),
        ),
    ]
