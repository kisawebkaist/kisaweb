# Generated by Django 3.0 on 2021-09-24 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia', '0004_auto_20210918_1923'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='video',
            name='slug',
        ),
    ]
