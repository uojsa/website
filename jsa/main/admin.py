from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from nested_admin import NestedModelAdmin, NestedTabularInline
from .models import Event, Container, Card, EventSession, ExecRole, Sponsor, UserProfile


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

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()

@admin.register(EventSession)
class EventSessionAdmin(admin.ModelAdmin):
    # right-side container notes
    inlines = [SessionNoteInline]

    # Columns shown on the "Event Sessions" list page
    list_display = ("name", "event", "date", "start_time", "end_time", "location", "created_by")

    # Sidebar filters on the right
    list_filter = ("date", "event")

    # Search bar at the top (searches event name or location)
    search_fields = ("event__name", "location")

    # Non-editable tracking fields
    readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")

    # makes the box smaller than default
    formfield_overrides = {
        models.TextField: {
            "widget": Textarea(attrs={"rows": 3, "cols": 60})
        },
    }
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()

# other models
admin.site.register(ExecRole)
admin.site.register(Sponsor)
