# Generated by Django 3.0 on 2022-02-09 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aboutus', '0010_auto_20211121_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basemember',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]