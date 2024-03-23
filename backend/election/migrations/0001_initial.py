# Generated by Django 4.2.11 on 2024-03-24 02:40

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.query


class Migration(migrations.Migration):
    initial = True

    dependencies = [
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
                (
                    "start_datetime",
                    models.DateTimeField(blank=True, default=datetime.datetime.now),
                ),
                ("end_datetime", models.DateTimeField()),
                ("intro_msg", models.JSONField(blank=True, default=dict)),
                ("instructions", models.JSONField(blank=True, default=dict)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="election/img"),
                ),
                ("debate_url", models.CharField(blank=True, max_length=512, null=True)),
                (
                    "slug",
                    models.SlugField(blank=True, help_text="You can leave this blank."),
                ),
                ("is_open_public", models.BooleanField(blank=True, default=False)),
                ("results_out", models.BooleanField(blank=True, default=False)),
                (
                    "results_cache_datetime",
                    models.DateTimeField(blank=True, default=datetime.datetime.now),
                ),
                ("results_archived", models.BooleanField(blank=True, default=False)),
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
                        default=django.db.models.query.QuerySet.latest,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="election.election",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
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
                ("manifesto", models.JSONField(blank=True, default=dict)),
                ("speech_url", models.CharField(blank=True, max_length=512, null=True)),
                ("kisa_history", models.JSONField(blank=True, default=dict)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="election/img"),
                ),
                ("slug", models.SlugField(blank=True, max_length=120)),
                ("is_open_public", models.BooleanField(default=False)),
                ("num_votes", models.PositiveIntegerField(default=0)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "election",
                    models.ForeignKey(
                        default=django.db.models.query.QuerySet.latest,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="election.election",
                    ),
                ),
            ],
            options={
                "unique_together": {("account", "election")},
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
                        on_delete=django.db.models.deletion.CASCADE,
                        to="election.candidate",
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
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "election")},
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
                        on_delete=django.db.models.deletion.CASCADE,
                        to="election.election",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "election")},
            },
        ),
    ]
