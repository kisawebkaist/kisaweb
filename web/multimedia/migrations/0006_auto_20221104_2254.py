# Generated by Django 3.0 on 2022-11-04 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia', '0005_auto_20210924_1807'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='file',
        ),
        migrations.AddField(
            model_name='multimedia',
            name='multiple_images',
            field=models.FileField(blank=True, null=True, upload_to='zips'),
        ),
    ]
