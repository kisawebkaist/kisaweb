# Generated by Django 3.0 on 2021-09-13 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0014_auto_20210731_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title_category',
            field=models.CharField(blank=True, max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='faq',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='faqs', to='faq.Category'),
        ),
    ]
