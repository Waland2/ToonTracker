from django.contrib import admin

from .models import TempCartoon

@admin.register(TempCartoon)
class TempCartoonAdmin(admin.ModelAdmin):
    list_display = ['type_of_request', 'rus_title', 'eng_title', 'status', 'type']
    list_filter = ['type_of_request', 'rus_title', 'eng_title', 'status', 'type']
    search_fields = ['rus_title', 'eng_title']
    ordering = ['id']