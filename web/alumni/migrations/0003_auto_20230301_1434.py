# Generated by Django 3.0 on 2023-03-01 05:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0002_auto_20230228_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumni',
            name='joined_year',
            field=models.IntegerField(default=2004, validators=[django.core.validators.MinValueValidator(2004), django.core.validators.MaxValueValidator(2023)]),
        ),
        migrations.AlterField(
            model_name='alumni',
            name='separated_year',
            field=models.IntegerField(default=2023, help_text='If the alumni only worked for one season please enter the same year as joined year.', validators=[django.core.validators.MinValueValidator(2004), django.core.validators.MaxValueValidator(2023)]),
        ),
    ]
