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
    thumbnail = models.ImageField(upload_to="event_thumbnails/", blank=True, null=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def eventLengthHours(self):
        duration = self.end_datetime - self.start_datetime
        return round(duration.total_seconds() / 3600)

    def formatted_start_datetime(self):
        start_datetime = timezone.localtime(self.start_datetime)
        date_part = start_datetime.strftime("%B %d")
        time_part = start_datetime.strftime("%I:%M %p").lstrip("0")
        return f"{date_part} • {time_part}"