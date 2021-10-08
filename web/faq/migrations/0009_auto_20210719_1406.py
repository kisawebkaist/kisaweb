# Generated by Django 3.0 on 2021-07-19 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0008_auto_20210719_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_category', models.CharField(choices=[('Student life', 'Student'), ('Academics', 'Academics'), ('Advices', 'Advices'), ('nothing', 'nothing')], max_length=63, verbose_name='Type')),
            ],
        ),
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='faq.Category'),
        ),
    ]
