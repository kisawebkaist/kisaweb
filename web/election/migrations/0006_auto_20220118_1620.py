# Generated by Django 3.0 on 2022-01-18 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0005_auto_20220111_0606'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='election',
            options={'permissions': [('see_election_results', 'Can view election results anytime'), ('preview_election', 'Can preview the election before it is published'), ('voting_exception', 'Can vote in election even if the user does not satisfy the voting conditions')]},
        ),
    ]