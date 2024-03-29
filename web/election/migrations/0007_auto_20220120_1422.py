# Generated by Django 3.0 on 2022-01-20 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0006_auto_20220118_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='consider_debate_participation',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AddField(
            model_name='voter',
            name='joined_debate',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
