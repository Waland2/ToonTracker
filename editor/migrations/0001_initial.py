# Generated by Django 5.1.1 on 2024-10-05 15:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0033_profile_is_blocked'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NewModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TempCartoon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_request', models.CharField(choices=[('add', 'Добавление'), ('edit', 'Редактирование')], default='edit', max_length=4)),
                ('eng_title', models.CharField(max_length=255)),
                ('rus_title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('rating', models.FloatField(default=7.0)),
                ('number_of_ratings', models.IntegerField(default=1)),
                ('start_year', models.DateField(blank=True, null=True)),
                ('end_year', models.DateField(blank=True, null=True)),
                ('number_of_seasons', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('number_of_series', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('cover', models.ImageField(blank=True, null=True, upload_to='covers')),
                ('is_published', models.BooleanField(default=True, null=True)),
                ('age_restrictions', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('creators', models.SmallIntegerField(blank=True, null=True)),
                ('genres', models.ManyToManyField(blank=True, null=True, to='main.cartoonsgenres')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main.cartoonsstatus')),
                ('studios', models.ManyToManyField(blank=True, null=True, to='main.studios')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main.cartoonstypes')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
            },
        ),
    ]
