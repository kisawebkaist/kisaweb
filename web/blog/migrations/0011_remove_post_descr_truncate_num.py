# Generated by Django 3.0 on 2021-01-19 23:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20210120_0654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='descr_truncate_num',
        ),
    ]
