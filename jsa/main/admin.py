from django.contrib import admin

# Register your models here.
from .models import Event

class EventAdmin(admin.ModelAdmin):
    search_fields = ['title', 'description']
    list_filter = ['category']
    list_display = ['title', 'category', 'location', 'start_datetime', 'end_datetime']

admin.site.register(Event, EventAdmin)