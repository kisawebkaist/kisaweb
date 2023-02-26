# Generated by Django 3.0 on 2022-11-18 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0011_auto_20220120_1804'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='election',
            name='general_vote_weight',
        ),
        migrations.RemoveField(
            model_name='election',
            name='kisa_in_debate_vote_explanation',
        ),
        migrations.RemoveField(
            model_name='election',
            name='kisa_no_debate_weight',
        ),
        migrations.RemoveField(
            model_name='election',
            name='kisa_vote_explanation',
        ),
        migrations.RemoveField(
            model_name='election',
            name='kisa_yes_debate_weight',
        ),
        migrations.RemoveField(
            model_name='election',
            name='non_kisa_vote_explanation',
        ),
        migrations.RemoveField(
            model_name='election',
            name='show_debate_participation',
        ),
        migrations.RemoveField(
            model_name='election',
            name='use_the_manual_weights',
        ),
        migrations.RemoveField(
            model_name='election',
            name='weighted_vote_explanation',
        ),
        migrations.AddField(
            model_name='election',
            name='adjusted_votes_explanation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='election',
            name='adjusted_votes_formula',
            field=models.TextField(default='((kivm) / (kiva) + (kovm + nkvm) / (kova + nkva)) * 0.5', help_text='The variables allowed to be used: kiva, kivm, kova, kovm, nkva and nkvm', null=True),
        ),
        migrations.AddField(
            model_name='election',
            name='kisa_in_debate_member_email_list',
            field=models.TextField(blank=True),
        ),
    ]
