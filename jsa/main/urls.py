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


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)