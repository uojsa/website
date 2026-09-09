from django.db.models import Prefetch
from django.utils import timezone
from django.shortcuts import render, get_object_or_404

from .models import Event, EventSession

# Create your views here.

def home(request):
    return render(request, "main/home.html")

def jcg(request):
    return render(request, "main/jcg.html")

def team(request):
    return render(request, "main/team.html")

## Event Views ##

def event_list(request):
    sessions = get_object_or_404(
        Event.objects.prefetch_related(
            Prefetch(
                "sessions", queryset=EventSession.objects.order_by("-date", "-id")
            )
        )
    )
    # Fetch the single latest open EventSession directly for an event
    latest_open = (
        EventSession.objects.filter(registration_deadline__gt=timezone.now())
        .order_by("-date", "-id")
        .first()  # .first() is fine here because this is NOT inside Prefetch()
    )

    context = {
        "sessions" : sessions,
        "latest_open" : latest_open
    }
    return render(request, "event_list.html", {"context" : context})

def event_detail(request, event_slug):
    event = get_object_or_404(
        Event.objects.prefetch_related(
            Prefetch(
                "sessions", queryset=EventSession.objects.order_by("-date", "-id")
            )
        ),
        slug=event_slug,
    )
    return render(request, "event_detail.html", {"event" : event})

def event_register(request, id):
    session = get_object_or_404(EventSession, pk=id)
    return render(request, "event_register.html", {"session" : session})

## Archive Views ##

def archive_list(request):
    return render(request, "archive_list.html")

def archive_detail(request, semester, event_slug):
    return HttpResponse(f"Archive: {semester}/{event_slug}")
