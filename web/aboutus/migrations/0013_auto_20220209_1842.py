# Generated by Django 3.0 on 2022-02-09 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_divisionitem'),
        ('aboutus', '0012_auto_20220208_1900'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DivisionDescription',
            new_name='Division',
        ),
        migrations.AddField(
            model_name='member',
            name='division',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='aboutus.Division'),
        ),
    ]
