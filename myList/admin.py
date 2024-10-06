from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(MyListStatus)
admin.site.register(MyListScores)

@admin.register(MyListObject)
class MyListObjectAdmin(admin.ModelAdmin):
    list_display = ['user', 'cartoon', 'score', 'watch_status']
    list_filter = ['user', 'cartoon', 'score', 'watch_status']