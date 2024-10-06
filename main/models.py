from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

def profile_image_path(instance, filename):
    return f"profile_image/{instance.user.id}.png"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to=profile_image_path, blank=True)
    
    description = models.TextField(blank=True)
    is_list_public = models.BooleanField(default=True)
    is_cover_in_list = models.BooleanField(default=True)

    is_blocked = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Cartoons(models.Model):
    eng_title = models.CharField(max_length=255) 
    rus_title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    type = models.ForeignKey('CartoonsTypes', models.PROTECT, null=True)
    status = models.ForeignKey('CartoonsStatus', models.PROTECT, null=True)

    rating = models.FloatField(default=7.0)
    number_of_ratings = models.IntegerField(default=1)

    start_year = models.DateField(blank=True, null=True)
    end_year = models.DateField(blank=True, null=True)

    number_of_seasons = models.PositiveSmallIntegerField(blank=True, null=True)
    number_of_series = models.PositiveSmallIntegerField(blank=True, null=True)

    genres = models.ManyToManyField('CartoonsGenres', blank=True, null=True)

    studios = models.ManyToManyField('Studios', blank=True, null=True)
    cover = models.ImageField(upload_to="covers", blank=True, null=True)

    is_published = models.BooleanField(default=True, null=True)

    age_restrictions = models.PositiveSmallIntegerField(blank=True, null=True)
    creators = models.SmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.rus_title} / {self.eng_title}"
    
    def get_absolute_url(self):
        return f'/cartoon/{self.id}/{self.eng_title.replace(" ", "-")}'

    class Meta:
        verbose_name = 'Мультсериал'
        verbose_name_plural = 'Мультсериалы'
        ordering = ["-rating"]


class CartoonsGenres(models.Model):
    name = models.CharField(max_length=50)
    eng_name = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/cartoons/?genres={self.eng_name}'

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ["name"]


class CartoonsStatus(models.Model):
    name = models.CharField(max_length=50)
    eng_name = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        ordering = ["name"]

class CartoonsTypes(models.Model):
    name = models.CharField(max_length=50)
    eng_name = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

class Studios(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/cartoons/?studios={self.name}'

    class Meta:
        verbose_name = 'Студия'
        verbose_name_plural = 'Студии'