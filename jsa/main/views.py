from django.db.models import Prefetch
from django.utils import timezone
from django.shortcuts import render, get_object_or_404

from .models import Event, EventSession, Album, Photo

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

def archive_list(request, year=None, semester=None):
    # get albums according to URL
    albums = Album.objects.order_by("-session__date").prefetch_related("photos").all() 
    if year is not None:
        albums = Album.objects.select_related("session").filter(session__date__year=year).order_by("-session__date").prefetch_related("photos").all()
        if semester is not None:
            albums = albums.filter(semester_slug=semester)

    # get all distinct years
    years = (
        Album.objects.values_list("session__date__year", flat=True)
        .distinct()
        .order_by("-session__date__year")
    )

    # returned context to template
    context = {
        "albums": albums,
        "years": years,
        "selected_year": year
    }

    return render(request, "archive_list.html", context)

def archive_detail(request, year, semester, event_slug):
    album = get_object_or_404(
        Album.objects.select_related("session").prefetch_related(
            Prefetch("photos", queryset=Photo.objects.order_by("-id"))
        ),
        session__date__year=year,
        semester_slug=semester,
        event_slug=event_slug,
    )
    return render(request, "archive_detail.html", {"album" : album})
