# Generated by Django 3.0 on 2022-10-01 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footer',
            name='email',
            field=models.EmailField(max_length=50),
        ),
    ]
