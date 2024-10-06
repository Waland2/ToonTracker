from celery import Celery
import os
from django.conf import settings
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toontracker.settings')

app = Celery('toontracker')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'calculate_cartoons_rating': {
        'task': 'myList.tasks.calculate_cartoons_rating', 
        'schedule': timedelta(hours=4)
    },
}

app.conf.timezone = 'UTC'
