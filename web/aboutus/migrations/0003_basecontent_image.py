# Generated by Django 3.0 on 2021-11-03 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aboutus', '0002_auto_20211026_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='basecontent',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
