# Generated by Django 5.1.1 on 2024-10-05 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_cartoons_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartoons',
            name='test',
        ),
    ]
