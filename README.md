# ToonTracker
ToonTracker is a Russian-language website for tracking watched cartoons, similar to MyAnimeList. Users can add new works, edit existing ones, track their viewing progress, search for cartoons by title, and share their watchlists with friends.

# Launch
```
1) pip install -r requirements.txt
2) edit toontracker/settings.py
3) python manage.py migrate
4) celery -A toontracker worker -l info
5) celery -A toontracker beat -l info
6) python manage.py runserver
```