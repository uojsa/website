from django.urls import path

from . import views

app_name = 'archive'

urlpatterns = [
    # / index page that shows events as cards, divided per semester 
    path("", views.index, name="index"),

    # dedicated page for a single event's photos
    path("<slug:semester>/<slug:event_slug>", views.event, name="event"),
]
