from django.urls import path

from . import views

urlpatterns = [
    ## Static Routes ##
    # The "/" or "/home" path, home page
    path("", views.home, name="home"),
    path("home", views.home, name="home"),

    ## Events Routes ##
    #  1. The Events Calendar page / List of all upcoming events
    #  2. The individual event sign up page (Date, time, location, etc.)
    #  3. The event general detail page (What it"s about, frequency, etc.)
    path("events/calendar/", views.event_list, name="event_list"),
    path("events/<int:id>/register/", views.event_register, name="event_register"),
    path("events/<slug:event_slug>/", views.event_detail, name="event_detail"),

    ## Archive Routes ##
    # index page that shows events as cards, divided per semester
    path("archive/", views.archive_list, name="archive_list"),
    # dedicated page for a single event"s photos
    path("archive/<slug:semester>/<slug:event_slug>", views.archive_detail, name="archive_detail"),

    # The "/team" path, about page
    path("team", views.team, name="team"),
]
