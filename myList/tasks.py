from toontracker.celery import app

from .models import MyListObject
from main.models import Cartoons

@app.task
def calculate_cartoons_rating():
    cartoons = list(Cartoons.objects.all())
    for cartoon in cartoons:
        ml_objects = MyListObject.objects.filter(cartoon=cartoon)

        # by default all cartoons have rating 7 with 1 review
        score = 7
        scores_count = len(ml_objects) + 1

        for obj in ml_objects:
            score += obj.score.value
        
        final_score = score / max(scores_count, 1)

        cartoon.rating = final_score
        cartoon.number_of_ratings = scores_count
        cartoon.save()


    MyListObject.objects.all()