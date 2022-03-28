# Generated by Django 3.0 on 2021-11-04 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aboutus', '0005_delete_activemember'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='internalboardmember',
            options={'ordering': ['-year', 'semester', 'the_order', 'position', 'name']},
        ),
        migrations.AlterModelOptions(
            name='member',
            options={'ordering': ['-year', 'semester', 'position', 'name']},
        ),
        migrations.AddField(
            model_name='basemember',
            name='the_order',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
        ),
    ]
