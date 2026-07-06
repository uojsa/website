from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("archive", views.archive, name="archive"),
    path("calendar", views.calendar, name="calendar"),
    path("jcg", views.jcg, name="jcg"),
    path("team", views.team, name="team"),
]