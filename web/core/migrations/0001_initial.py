# Generated by Django 3.0 on 2021-03-11 06:08

from django.db import migrations, models
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourseUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True)),
                ('class_id', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmptyQueryset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('events', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Footer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kisa_text', models.CharField(blank=True, max_length=500)),
                ('location', models.CharField(max_length=80)),
                ('phnum_eng', phone_field.models.PhoneField(max_length=31)),
                ('phnum_kor', phone_field.models.PhoneField(max_length=31)),
                ('email', models.EmailField(max_length=20)),
                ('fb_link', models.URLField(blank=True)),
                ('insta_link', models.URLField(blank=True)),
                ('yt_link', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseResources',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_id', models.CharField(max_length=255, unique=True)),
                ('class_name', models.CharField(max_length=255)),
                ('url', models.ManyToManyField(to='core.CourseUrl')),
            ],
        ),
    ]
