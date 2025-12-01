from django.db import models
from django.shortcuts import render
from django.utils import timezone

from events.models import Event


# Create your views here.
def organizer_dashboard(request):
    today = timezone.now().date()

    counts = Event.objects.aggregate(
        total_participants=models.Count("participants", distinct=True),
        total_events=models.Count("id", distinct=True),
        upcoming_events=models.Count(
            "id", filter=models.Q(event_date__gt=today), distinct=True
        ),
        past_events=models.Count(
            "id", filter=models.Q(event_date__lt=today), distinct=True
        ),
    )

    context = {"count": counts}
    return render(request, "dashboard/organizer-dashboard.html", context)


def view_all(request):
    return render(request, "view-all.html", {"view_name": "Event"})
