from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, "archive/index.html")

def event(request, semester, event_slug):
    return HttpResponse(f"Archive: {semester}/{event_slug}")
