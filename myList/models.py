from django.db import models
from main.models import Cartoons, User

class MyListStatus(models.Model):
    name = models.CharField(max_length=50)
    priority_in_list = models.SmallIntegerField(blank=True, null=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
    
class MyListScores(models.Model):
    value = models.SmallIntegerField()
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"({self.value}) {self.name}"

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'


class MyListObject(models.Model):
    cartoon = models.ForeignKey(Cartoons, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    watch_status = models.ForeignKey(MyListStatus, on_delete=models.CASCADE, default=1)
    score = models.ForeignKey(MyListScores, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.TextField(max_length=750, blank=True)    
    times_rewatched = models.SmallIntegerField(default=1)

    class Meta:
        verbose_name = 'Обьект'
        verbose_name_plural = 'Обьекты'


