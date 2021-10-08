# Generated by Django 3.0 on 2021-05-30 09:17

from django.conf import settings
from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True)),
                ('location', models.CharField(blank=True, default='TBA', max_length=100)),
                ('is_link', models.BooleanField(default=False, verbose_name='Event is online (i.e. has link)')),
                ('link', models.URLField(blank=True, default='TBA')),
                ('event_start_datetime', models.DateTimeField()),
                ('event_end_datetime', models.DateTimeField()),
                ('registration_start_datetime', models.DateTimeField(blank=True, null=True)),
                ('registration_end_datetime', models.DateTimeField(blank=True, null=True)),
                ('max_occupancy', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('current_occupancy', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('important_message', models.CharField(blank=True, max_length=200)),
                ('description', tinymce.models.HTMLField()),
                ('descr_truncate_num', models.PositiveSmallIntegerField(blank=True, default=50)),
                ('image', models.ImageField(blank=True, null=True, upload_to='events/img')),
                ('image_height', models.PositiveSmallIntegerField(blank=True, default=260)),
                ('image_width', models.PositiveSmallIntegerField(blank=True, default=260)),
                ('has_registration_form', models.BooleanField(default=False)),
                ('registration_form_src', models.CharField(blank=True, max_length=255)),
                ('participants', models.ManyToManyField(blank=True, related_name='faq_participants', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
