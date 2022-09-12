# Generated by Django 3.0 on 2022-03-21 12:18

from django.db import migrations, models
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
            name='Navbar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kisa_voice_link', models.URLField(blank=True)),
                ('kisa_books_link', models.URLField(blank=True)),
                ('internships_link', models.URLField(blank=True)),
                ('kaist_ara_link', models.URLField(blank=True)),
                ('course_resources_link', models.URLField(blank=True)),
                ('kisa_room_reservation_link', models.URLField(blank=True)),
            ],
        ),
    ]
