# Generated by Django 3.0 on 2022-03-21 12:18

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True)),
                ('desc', tinymce.models.HTMLField(null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('the_order', models.PositiveIntegerField(db_index=True, default=0, editable=False)),
            ],
            options={
                'ordering': ['the_order'],
            },
        ),
        migrations.CreateModel(
            name='BaseMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('year', models.PositiveIntegerField(null=True)),
                ('semester', models.CharField(choices=[('Spring', 'Spring'), ('Fall', 'Fall')], max_length=10, null=True)),
                ('sns_link', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ConstitutionPDF',
            fields=[
                ('basecontent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='aboutus.BaseContent')),
                ('constitution_file', models.FileField(null=True, upload_to='constitution')),
            ],
            options={
                'abstract': False,
            },
            bases=('aboutus.basecontent',),
        ),
        migrations.CreateModel(
            name='DivisionContent',
            fields=[
                ('basecontent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='aboutus.BaseContent')),
                ('division_name', models.CharField(max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('aboutus.basecontent',),
        ),
        migrations.CreateModel(
            name='MainContent',
            fields=[
                ('basecontent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='aboutus.BaseContent')),
            ],
            options={
                'abstract': False,
            },
            bases=('aboutus.basecontent',),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('basemember_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='aboutus.BaseMember')),
                ('division', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='members', related_query_name='member', to='aboutus.DivisionContent')),
            ],
            bases=('aboutus.basemember',),
        ),
        migrations.CreateModel(
            name='InternalBoardMember',
            fields=[
                ('basemember_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='aboutus.BaseMember')),
                ('position', models.CharField(choices=[('President', 'President'), ('Division Head', 'Division Head'), ('Secretary', 'Secretary')], max_length=100, null=True)),
                ('the_order', models.PositiveIntegerField(db_index=True, default=0, editable=False)),
                ('division', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='aboutus.DivisionContent')),
            ],
            options={
                'ordering': ['the_order'],
            },
            bases=('aboutus.basemember', models.Model),
        ),
    ]
