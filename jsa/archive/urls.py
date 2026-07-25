from django.urls import path

from . import views

app_name = 'archive'

urlpatterns = [
    # index page that shows all JCG photos for that semester
    path("<slug:semester>/", views.index, name="index"),

    # dedicated page for a single large event's photos
    path("<slug:semester>/<slug:event_slug>", views.big_event, name="big-event"),
]
