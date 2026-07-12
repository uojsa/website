from django.http import HttpResponse

def event_list(request):
    return HttpResponse("Event List: Placeholder.")

def event_detail(request, event_slug):
    return HttpResponse(f"Event Details: {event_slug}")

def event_signup(request, id):
    return HttpResponse("Event Sign Up: Placeholder")
