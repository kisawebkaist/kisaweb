# Generated by Django 3.0 on 2022-09-06 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('url_shortener', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UrlVisitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=15, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UrlVisit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit_count', models.BigIntegerField(default=0)),
                ('visited_url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='url_shortener.UrlShortener')),
                ('visitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='url_shortener.UrlVisitor')),
            ],
            options={
                'unique_together': {('visitor', 'visited_url')},
            },
        ),
        migrations.AddField(
            model_name='urlshortener',
            name='visitors',
            field=models.ManyToManyField(through='url_shortener.UrlVisit', to='url_shortener.UrlVisitor'),
        ),
    ]
