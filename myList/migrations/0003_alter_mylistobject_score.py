# Generated by Django 4.2.7 on 2023-12-18 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myList', '0002_alter_mylistobject_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mylistobject',
            name='score',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myList.mylistscores'),
        ),
    ]
