from django.http import HttpResponse


def index(request, semester):
    return HttpResponse(f"Archive: {semester}")

def big_event(request, semester, event_slug):
    return HttpResponse(f"Archive: {semester}/{event_slug}")
