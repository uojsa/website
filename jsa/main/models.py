from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class IconChoices(models.TextChoices):
    INFO = "info", "Info / Note"
    QUESTION = "question", "Question / What is?"
    CLOCK = "clock", "Clock / Time"
    LOCATION = "location", "Map / Location"
    BELL = "bell", "Bell / Notification"
    CALENDAR = "calendar", "Calendar"
    STAR = "star", "Star / Featured"
    MEETUP = "users", "People / Gathering"
    NONE = "none", "None"

# ==========================================
# 1. EXEC ROLES (Managed by Superusers)
# ==========================================
class ExecRole(models.Model):
    title = models.CharField(
        max_length=50,
        unique=True,
        help_text="Role title (e.g., President, VP Events)",
    )
    order = models.PositiveIntegerField(
        default=0, help_text="Sort order for 'Meet the Team' page"
    )

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Exec Role"
        verbose_name_plural = "Exec Roles"

    def __str__(self):
        return self.title


# ==========================================
# 2. USER PROFILE
# ==========================================
class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    role = models.ForeignKey(
        ExecRole,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="execs",
    )

    def __str__(self):
        role_name = self.role.title if self.role else "General Member"
        return f"{self.user.get_full_name() or self.user.username} - {role_name}"


# Auto-create or save UserProfile whenever a User is created/updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # For existing users, safely get or create profile before calling save
        UserProfile.objects.get_or_create(user=instance)
        instance.profile.save()

# ==========================================
# 3. SPONSORS
# ==========================================
class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="sponsor_logos/", blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

# ==========================================
# 4. EVENTS
# ==========================================
class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ("CULTURE", "Culture"),
        ("LANGUAGE", "Language"),
        ("COMMUNITY", "Community"),
        ("FESTIVAL", "Festival"),
    ]

    class DayOfWeek(models.IntegerChoices):
        MONDAY = 1, "Monday"
        TUESDAY = 2, "Tuesday"
        WEDNESDAY = 3, "Wednesday"
        THURSDAY = 4, "Thursday"
        FRIDAY = 5, "Friday"
        SATURDAY = 6, "Saturday"
        SUNDAY = 7, "Sunday"

    class Frequency(models.IntegerChoices):
        EVERY_WEEK = 1, "Every Week"
        EVERY_OTHER_WEEK = 2, "Every Other Week"
        MONTHLY = 3, "Every Month"
        EVERY_SEM = 4, "Every Semester"
        EVERY_FALL = 5, "Every Fall Semester"
        EVERY_WINTER = 6, "Every Winter Semester"
        EVERY_SUM = 7, "Every Summer Semester" 
        YEARLY = 8, "Every Year"
        ONCE = 9, "One-off"

    name = models.CharField(max_length=200)
    slug = models.SlugField(
        unique=True,
        help_text="URL string (e.g., japanese-conversation-group)",
    ) 
    banner = models.TextField()
    event_type = models.CharField(
        max_length=20, choices=EVENT_TYPE_CHOICES, default="CULTURE"
    )
    day_of_week = models.PositiveSmallIntegerField(
        choices=DayOfWeek.choices,
        blank=True,
        null=True,
        help_text="Optional. Day of the week for recurring schedules.",
    )
    frequency = models.PositiveSmallIntegerField(
        choices=Frequency.choices,
        default=Frequency.EVERY_WEEK,
        null=False,
        help_text="Determines formatting in event page right-side detail card." 
    )
    start_time = models.TimeField(
        blank=True,
        null=True, 
        help_text="Optional. Leave blank if the exact time is TBD.",
    )
    end_time = models.TimeField(
        blank=True,
        null=True,
        help_text="Optional. Leave blank if the exact time is TBD.",
    )
    location = models.CharField(
        max_length=50,
        default="STEM Complex",
        blank=True,
        help_text="Optional. Leave blank if the exact location is TBD."
    )
    room = models.CharField(
        max_length=50,
        default="STEM 404",
        blank=True,
        help_text="Optional. Leave blank if room is TBD."
    )
    note = models.CharField(
        max_length=40,
        default="See you there!",
        help_text="'Note' field in event main page."
    )
    sponsors = models.ManyToManyField(
        Sponsor,
        blank=True,
        related_name="events"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="events_created",
    )
    last_edited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="events_edited",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def latest_open_session(self):
        """Finds the upcoming/active session that is still open for registration."""
        # Filters for sessions where date is today or in the future
        upcoming_sessions = self.sessions.filter(
            date__gte=timezone.now().date()
        ).order_by("date", "start_time")

        # Returns the first session where is_open is True
        for session in upcoming_sessions:
            if session.is_open:
                return session

        return None

    def __str__(self):
        return f"{self.name}"

# ==========================================
# Event Page UI Container
# ==========================================
class Container(models.Model):
    event = models.ForeignKey(
        Event,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="containers"
    )   
    icon = models.CharField(
        max_length=20,
        choices=IconChoices.choices,
        default=IconChoices.CALENDAR,
        help_text="Select an icon to display on event cards and banners.",
    )
    header = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.header

class EventSession(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="sessions"
    )
    name = models.CharField(
        max_length=50, default="Session"
    )   
    banner = models.TextField(
        blank=True,
        help_text="Optional. If empty, will default to parent event banner."
    )
    class Meta:
        # Singular title (used on detail pages, object deletion forms, etc.)
        verbose_name = "Session"

        # Plural title (used in sidebar tabs, list headings, breadcrumbs)
        verbose_name_plural = "Sessions"

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    registration_deadline = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Event register button marked as  'Not Available Yet' after deadline. Leave empty for Drop-in / Walk-in events."
    )
    location = models.CharField(
        max_length=50,
        help_text="Building / Park. (e.g., STEM Complex)"
    )
    room = models.CharField(
        max_length=50,
        blank=True,
        help_text="Optional. (e.g., STEM 404)"
    )
    signup_link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Optional. Leave empty for Drop-in / Walk-in events." 
    )
    poster_image = models.ImageField(
        upload_to="event_posters/", blank=True, null=True
    )
    cost = models.DecimalField(
        max_digits=2,
        decimal_places=2,
        default=0.00,
        help_text="Leave as 0.00 to label as Free."
    )
    capacity = models.PositiveIntegerField(
        default=30,
        help_text="Leave as 0 for sessions  with no capacity restriction."
    )
    featured = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Check this box to highlight this session on the home page or in the calendar banner."
    )
     
    # analytics
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Audit Trail Fields
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="created_occurrences",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="updated_occurrences",
    )

    @property
    def is_open(self):
        """Returns True if the current time is before the cutoff/closing time."""
        now = timezone.now()

        # If a specific registration deadline is set, check against it
        if self.registration_deadline:
            return now < self.registration_deadline

        # If no date is set, assume registration is open
        return True

    def __str__(self):
        return f"{self.name} ({self.date})"

class Card(models.Model):
    container = models.ForeignKey(
        Container,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="cards"
    )
    event_session = models.ForeignKey(
        EventSession,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="notes"
    )
    icon = models.CharField(
        max_length=20,
        choices=IconChoices.choices,
        default=IconChoices.CALENDAR,
        help_text="Select an icon to display to the left of the text."
    )
    header = models.CharField(default="Header Text")
    text = models.TextField(default="Loren Ipsum")

    def __str__(self):
        return self.header
