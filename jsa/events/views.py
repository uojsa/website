from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, "events/calendar.html")

def detail(request, event_slug):
    return render(request, "events/detail.html", {"event" : event_slug})

def register(request, id):
    return HttpResponse("Event Sign Up: Placeholder")
