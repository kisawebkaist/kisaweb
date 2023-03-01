# Generated by Django 3.0 on 2023-02-28 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='KISA_Positions',
            new_name='Kisa_Position',
        ),
        migrations.AlterField(
            model_name='alumni',
            name='current_contact',
            field=models.URLField(blank=True, help_text='Current contact of the Alumni. Be sure to ask the alumni for permission to post it.', null=True),
        ),
        migrations.AlterField(
            model_name='alumni',
            name='joined_year',
            field=models.IntegerField(default=2023),
        ),
        migrations.AlterField(
            model_name='alumni',
            name='separated_season',
            field=models.CharField(blank=True, choices=[('Spring', 'Spring'), ('Summer', 'Summer'), ('Fall', 'Fall'), ('Winter', 'Winter')], help_text='If the alumni only worked for one season please leave this part empty.', max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='alumni',
            name='separated_year',
            field=models.IntegerField(blank=True, help_text='If the alumni only worked for one season please leave this part empty.', null=True),
        ),
    ]
