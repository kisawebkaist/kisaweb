# Generated by Django 4.2.7 on 2023-11-26 19:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("faq", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="faq",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
