# Generated by Django 4.2.7 on 2023-12-01 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_cartoons_options_alter_cartoonsstatus_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartoonsstatus',
            name='eng_name',
        ),
        migrations.RemoveField(
            model_name='cartoonstypes',
            name='eng_name',
        ),
    ]
