# Generated by Django 3.0 on 2021-01-19 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20210119_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='descr_truncate_num',
            field=models.PositiveSmallIntegerField(blank=True, default=50),
        ),
    ]
