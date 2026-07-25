# polls/urls.py or events/urls.py
from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # The Landing page / List of all upcoming events
    path('', views.event_list, name='index'),

    # The individual event sign up page (Date, time, location, etc.)
    path('<int:id>/register/', views.event_signup, name='signup'),

    # The event general detail page (What it's about, frequency, etc.)
    path('<slug:event_slug>/', views.event_detail, name='detail')
]
