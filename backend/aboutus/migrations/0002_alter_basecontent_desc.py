# Generated by Django 4.2.11 on 2024-05-04 11:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("aboutus", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="basecontent",
            name="desc",
            field=models.JSONField(default=dict),
        ),
    ]
