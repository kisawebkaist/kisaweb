# Generated by Django 3.0 on 2021-12-23 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sso', '0003_delete_agreement'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('see_election_results', 'Can view election results anytime')]},
        ),
    ]