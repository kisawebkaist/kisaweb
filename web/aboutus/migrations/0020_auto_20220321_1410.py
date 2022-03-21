# Generated by Django 3.0 on 2022-03-21 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aboutus', '0019_auto_20220321_1403'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basemember',
            name='position',
        ),
        migrations.AddField(
            model_name='internalboardmember',
            name='position',
            field=models.CharField(choices=[('President', 'President'), ('Division Head', 'Division Head'), ('Secretary', 'Secretary')], max_length=100, null=True),
        ),
    ]
