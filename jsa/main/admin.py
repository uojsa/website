from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.db import models
from django.forms import Textarea
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from nested_admin import NestedModelAdmin, NestedTabularInline
from dragndrop_related.views import DragAndDropRelatedImageMixin
from .models import Event, Container, Card, EventSession, Album, Photo, ExecRole, Sponsor, UserProfile


# define an inline admin form for UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile / Executive Role"


# unregister the default User admin and register a custom one
admin.site.unregister(User)

# register new custom user model
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]

class SessionNoteInline(admin.TabularInline):
    model = Card
    extra = 0 
    exclude = ("container",)

    # custom labels to overrwrite Card(s)
    verbose_name = "Note"
    verbose_name_plural = "Notes"   
 
    # makes the box smaller than default
    formfield_overrides = {
        models.TextField: {
            "widget": Textarea(attrs={"rows": 1, "cols": 50})
        },
    }

class EventCardInline(NestedTabularInline):
    model = Card
    extra = 0
    exclude = ("event_session",)

    # makes the box smaller than default
    formfield_overrides = {
        models.TextField: {
            "widget": Textarea(attrs={"rows": 1, "cols": 50})
        },
    }

class EventContainerInline(NestedTabularInline):
    model = Container
    extra = 0
    inlines = [EventCardInline]

    # makes the box smaller than default
    formfield_overrides = {
        models.TextField: {
            "widget": Textarea(attrs={"rows": 4, "cols": 50})
        },
    }

@admin.register(Event)
class EventAdmin(NestedModelAdmin):
    list_display = ("name", "slug", "created_by")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description") 
    inlines = [EventContainerInline]

    # makes the box smaller than default
    formfield_overrides = {
        models.TextField: {
            "widget": Textarea(attrs={"rows": 3, "cols": 60})
        },
    }

    # Non-editable tracking fields
    readonly_fields = (
        "created_by_info",
        "last_edited_by_info"
    )

    @admin.display(description="Created By")
    def created_by_info(self, obj):
        if not obj.pk:
            return "-"

        user = obj.created_by.get_full_name() or obj.created_by.username if obj.created_by else "Unknown"

        if obj.created_at:
            # Format date: 'Oct 15, 2026, 2:30 PM'
            date_str = timezone.localtime(obj.created_at).strftime("%b %d, %Y, %I:%M %p")
            return f"{user} at {date_str}"

        return f"{user}"

    @admin.display(description="Last Edited By")
    def last_edited_by_info(self, obj):
        if not obj.pk:
            return "-"

        user = obj.last_edited_by.get_full_name() or obj.last_edited_by.username if obj.last_edited_by else "Unknown"

        if obj.last_edited_at:
            # Format date: 'Oct 15, 2026, 2:30 PM'
            date_str = timezone.localtime(obj.last_edited_at).strftime("%b %d, %Y, %I:%M %p")
            return f"{user} at {date_str}"

        return f"{user}"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()

@admin.register(EventSession)
class EventSessionAdmin(admin.ModelAdmin):
    # right-side container notes
    inlines = [SessionNoteInline]

    # Columns shown on the "Event Sessions" list page
    list_display = (
        "name",
        "date",
        "start_time",
        "end_time",
        "registration_deadline",
        "location",
        "last_edited_by"
    )

    # fields that show on actual admin page
    fields = [
        "event",
        "name",
        "banner",
        "date",
        "start_time",
        "end_time",
        "registration_deadline",
        "location",
        "room",
        "signup_link",
        "poster_image",
        "cost",
        "featured",
        "capacity",
        "created_by_info",
        "last_edited_by_info"
    ]
    # Sidebar filters on the right
    list_filter = ("date", "event")

    # Search bar at the top (searches event name or location)
    search_fields = ("event__name", "location")

    # Non-editable tracking fields
    readonly_fields = (
        "created_by_info",
        "last_edited_by_info"
    )

    # makes the box smaller than default
    formfield_overrides = {
        models.TextField: {
            "widget": Textarea(attrs={"rows": 3, "cols": 60})
        },
    }

    @admin.display(description="Created By")
    def created_by_info(self, obj):
        if not obj.pk:
            return "-"

        user = obj.created_by.get_full_name() or obj.created_by.username if obj.created_by else "Unknown"
        
        if obj.created_at:
            # Format date: 'Oct 15, 2026, 2:30 PM'
            date_str = timezone.localtime(obj.created_at).strftime("%b %d, %Y, %I:%M %p")
            return f"{user} at {date_str}"
            
        return f"{user}"

    @admin.display(description="Last Edited By")
    def last_edited_by_info(self, obj):
        if not obj.pk:
            return "-"
    
        user = obj.last_edited_by.get_full_name() or obj.last_edited_by.username if obj.last_edited_by else "Unknown"

        if obj.last_edited_at:
            # Format date: 'Oct 15, 2026, 2:30 PM'
            date_str = timezone.localtime(obj.last_edited_at).strftime("%b %d, %Y, %I:%M %p")         
            return f"{user} at {date_str}"
     
        return f"{user}"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.last_edited_by = request.user
        obj.save()

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 0
    can_delete = True
    show_change_link = False

@admin.register(Album)
class AlbumAdmin(DragAndDropRelatedImageMixin, admin.ModelAdmin):
    # overriding values for dragndrop library
    related_manager_field_name = "photos"
    related_model_field_name = "file"

    # columns shown on album list page
    list_display = ("session", "date", "num_photos", "created_by")

    # fields on album page
    fields = [
        "session",
        "full_slug",
        "date",
        "location",
        "description",
        "num_attendees",
        "tag_name",
        "additional_info_icon",
        "additional_info", 
        "created_by_info",
        "last_edited_by_info"
    ] 

    # filters
    list_filter = ("num_attendees", "session")

    # search
    search_fields = ("session__name", "date")

    # non-editable
    readonly_fields = (
        "full_slug",
        "date",
        "location",
        "created_by_info",
        "last_edited_by_info"
    )
 
    # inlines to add photos
    inlines = [PhotoInline]

    # makes the box smaller than default
    formfield_overrides = {
        models.TextField: {
            "widget": Textarea(attrs={"rows": 3, "cols": 50})
        },
    }

    @admin.display(description="Slug")
    def full_slug(self, obj):
        if obj.pk and obj.semester_slug and obj.event_slug:
            slug_val = f"{obj.semester_slug}/{obj.event_slug}"
        else:
            slug_val = "-"

        # Renders the help text in small gray text below the slug value
        help_text = (
            "Auto-generated URL path derived from session date and name."
        )
        return mark_safe(
            f"<div>{slug_val}<br>"
            f"<span style='color: #666; font-size: 11px;'>{help_text}</span></div>"
        )

    @admin.display(description="Date")
    def date(self, obj):
        if obj.pk and obj.session and obj.session.date:
            date_val = obj.session.date
        else:
            date_val = "-"

        # Renders the help text in small gray text below the slug value
        help_text = (
            "Auto-generated. Derived from session date."
        )
        return date_val
        return mark_safe(
            f"<div>{date_val}<br>"
            f"<span style='color: #666; font-size: 11px;'>{help_text}</span></div>"
        )
 
    @admin.display(description="Location")
    def location(self, obj):
        if obj.pk and obj.session and obj.session.location and obj.session.room:
            location_val = f"{obj.session.location} | {obj.session.room}"
        elif obj.pk and obj.session and obj.session.location:
            location_val = f"{obj.session.location}"
        else:
            location_val = "-"
        
        # Renders the help text in small gray text below the slug value
        help_text = (
            "Auto-generated. Derived from session location."
        )
        return mark_safe(
            f"<div>{location_val}<br>"
            f"<span style='color: #666; font-size: 11px;'>{help_text}</span></div>"
        )

    @admin.display(description="Number of Photos")
    def num_photos(self, obj):
        if obj.pk and obj.photos:
            photos_num = f"{obj.photos.count()}"
        else:
            photos_num = "None"

        return photos_num 

    @admin.display(description="Created By")
    def created_by_info(self, obj):
        if not obj.pk:
            return "-"

        user = obj.created_by.get_full_name() or obj.created_by.username if obj.created_by else "Unknown"
        
        if obj.created_at:
            # Format date: 'Oct 15, 2026, 2:30 PM'
            date_str = timezone.localtime(obj.created_at).strftime("%b %d, %Y, %I:%M %p")
            return f"{user} at {date_str}"
            
        return f"{user}"

    @admin.display(description="Last Edited By")
    def last_edited_by_info(self, obj):
        if not obj.pk:
            return "-"

        user = obj.last_edited_by.get_full_name() or obj.last_edited_by.username if obj.last_edited_by else "Unknown"
        
        if obj.last_edited_at:
            # Format date: 'Oct 15, 2026, 2:30 PM'
            date_str = timezone.localtime(obj.last_edited_at).strftime("%b %d, %Y, %I:%M %p")
            return f"{user} at {date_str}"
            
        return f"{user}"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.last_edited_by = request.user
        obj.save()

# other models
admin.site.register(ExecRole)
admin.site.register(Sponsor)
