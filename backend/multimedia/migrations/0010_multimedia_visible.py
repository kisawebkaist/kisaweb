# Generated by Django 3.0 on 2022-11-05 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia', '0009_auto_20221105_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='multimedia',
            name='visible',
            field=models.BooleanField(default=False, null=True),
        ),
    ]