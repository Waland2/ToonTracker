# Generated by Django 4.2.7 on 2023-12-06 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_alter_cartoons_end_year_alter_cartoons_start_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartoons',
            name='end_year',
        ),
        migrations.RemoveField(
            model_name='cartoons',
            name='start_year',
        ),
    ]
