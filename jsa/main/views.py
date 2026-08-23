from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "main/home.html")

def jcg(request):
    return render(request, "main/jcg.html")

def team(request):
    return render(request, "main/team.html")
