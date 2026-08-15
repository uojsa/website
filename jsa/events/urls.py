# polls/urls.py or events/urls.py
from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # The Events Calendar page / List of all upcoming events
    path('calendar/', views.index, name='index'),

    # The individual event sign up page (Date, time, location, etc.)
    path('<int:id>/register/', views.register, name='register'),

    # The event general detail page (What it's about, frequency, etc.)
    path('<slug:event_slug>/', views.detail, name='detail')
]
