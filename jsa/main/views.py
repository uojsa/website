from django.shortcuts import render

# Create your views here.
from .models import Event

def home(request):
    events = Event.objects.order_by('start_datetime')[:3]
    return render(request, "home.html", {"events": events})

def calendar(request):
    return render(request, "calendar.html")

def archive(request):
    return render(request, "archive.html")

def jcg(request):
    return render(request, "jcg.html")

def team(request):
    return render(request, "team.html")