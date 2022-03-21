# Generated by Django 3.0 on 2021-11-04 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aboutus', '0003_basecontent_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveMember',
            fields=[
                ('basemember_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='aboutus.BaseMember')),
            ],
            bases=('aboutus.basemember',),
        ),
    ]