# Generated by Django 4.2.7 on 2023-11-21 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myList', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mylistobject',
            options={'verbose_name': 'Обьект', 'verbose_name_plural': 'Обьекты'},
        ),
        migrations.AlterModelOptions(
            name='myliststatus',
            options={'verbose_name': 'Статус', 'verbose_name_plural': 'Статусы'},
        ),
    ]
