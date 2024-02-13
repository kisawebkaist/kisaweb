# Generated by Django 4.2.10 on 2024-02-10 13:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("sso", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Election",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_datetime", models.DateTimeField()),
                ("end_datetime", models.DateTimeField()),
                ("intro_msg", models.TextField()),
                ("instructions", models.TextField()),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="election/img"),
                ),
                ("debate_url", models.CharField(blank=True, max_length=512, null=True)),
                ("slug", models.SlugField()),
                ("is_open_public", models.BooleanField(default=False)),
                ("results_out", models.BooleanField(default=False)),
            ],
            options={
                "permissions": [
                    (
                        "preview_election",
                        "Can preview the election before it is published",
                    )
                ],
                "get_latest_by": "start_datetime",
            },
        ),
        migrations.CreateModel(
            name="VotingExceptionToken",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "election",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="election.election",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sso.kaistprofile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Candidate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("manifesto", models.JSONField()),
                ("speech_url", models.CharField(blank=True, max_length=512, null=True)),
                ("kisa_history", models.JSONField()),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="election/img"),
                ),
                ("slug", models.SlugField(max_length=150)),
                ("is_open_public", models.BooleanField(default=False)),
                ("num_votes", models.IntegerField(default=0)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "election",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="election.election",
                    ),
                ),
            ],
            options={
                "index_together": {("account", "election")},
            },
        ),
        migrations.CreateModel(
            name="Vote",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("vote_type", models.BooleanField(default=True)),
                (
                    "candidate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="voters",
                        to="election.candidate",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="votes",
                        to="sso.kaistprofile",
                    ),
                ),
            ],
            options={
                "index_together": {("user", "candidate")},
            },
        ),
        migrations.CreateModel(
            name="DebateAttendance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "election",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="election.election",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "index_together": {("user", "election")},
            },
        ),
    ]
