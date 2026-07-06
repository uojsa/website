from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "home.html")

def calendar(request):
    return render(request, "calendar.html")

def archive(request):
    return render(request, "archive.html")

def jcg(request):
    return render(request, "jcg.html")

def team(request):
    return render(request, "team.html")