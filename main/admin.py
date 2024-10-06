from django.contrib import admin
from .models import *

@admin.register(Cartoons)
class CartoonsAdmin(admin.ModelAdmin):
    list_display = ['rus_title', 'eng_title', 'status', 'rating', 'is_published']
    list_filter = ['rus_title', 'eng_title', 'status', 'rating', 'is_published']
    search_fields = ['rus_title', 'eng_title']
    ordering = ['id']

admin.site.register(Profile)
admin.site.register(CartoonsGenres)
admin.site.register(CartoonsTypes)
admin.site.register(CartoonsStatus)
admin.site.register(Studios)


# raw_id_fields = ['author'] Замена выпадающего списка на число (id)
    