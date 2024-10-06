from django.db import models
from main.models import Cartoons, CartoonsGenres, CartoonsStatus, CartoonsTypes, Studios, User

# Create your models here.
class NewModel(models.Model):
    pass
class TempCartoon(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    type_of_request = models.CharField(choices=[('add', 'Добавление'), ('edit', 'Редактирование')], max_length=4, default='edit')
    cartoon = models.ForeignKey(Cartoons, models.CASCADE, blank=True, null=True)

    eng_title = models.CharField(max_length=255) 
    rus_title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    type = models.ForeignKey(CartoonsTypes, models.PROTECT, null=True)
    status = models.ForeignKey(CartoonsStatus, models.PROTECT, null=True)

    rating = models.FloatField(default=7.0)
    number_of_ratings = models.IntegerField(default=1)

    start_year = models.DateField(blank=True, null=True)
    end_year = models.DateField(blank=True, null=True)

    number_of_seasons = models.PositiveSmallIntegerField(blank=True, null=True)
    number_of_series = models.PositiveSmallIntegerField(blank=True, null=True)

    genres = models.ManyToManyField(CartoonsGenres, blank=True, null=True)

    studios = models.ManyToManyField(Studios, blank=True, null=True)
    cover = models.ImageField(upload_to="covers", blank=True, null=True)

    is_published = models.BooleanField(default=True, null=True)

    age_restrictions = models.PositiveSmallIntegerField(blank=True, null=True)
    creators = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        # ordering = ["-rating"]
