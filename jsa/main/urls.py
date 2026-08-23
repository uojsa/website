from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # The '/' path, home page
    path("", views.home, name="home"),

    # The '/home' path, also home
    path("home", views.home, name="home"),

    # The '/team' path, about page
    path("team", views.team, name="team"),
]
