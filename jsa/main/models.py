from django.db import models
from django.utils import timezone

# Create your models here.

class Event(models.Model):
    # Core event info
    title = models.CharField(max_length=200, default="")
    description = models.TextField(default="")

    # Categorization (e.g., "WORKSHOP")
    category = models.CharField(max_length=100, blank=True, default="")

    # Scheduling
    start_datetime = models.DateTimeField(default=timezone.now)
    end_datetime = models.DateTimeField(default=timezone.now)

    # Location
    location = models.CharField(max_length=200, default="TBA")

    # Media (e.g., the food/calligraphy header image)
    thumbnail = models.ImageField(upload_to="event_headers/", blank=True, null=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)