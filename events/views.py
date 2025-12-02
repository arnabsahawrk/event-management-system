from django.db import models
from django.db.models import Case, IntegerField, Value, When
from django.db.models.functions import Extract
from django.shortcuts import render
from django.utils import timezone

from events.models import Category, Event


def organizer_dashboard(request):
    today = timezone.now().date()

    type = request.GET.get("type")

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

    events = Event.objects.select_related("category").all()
    todayEvents = events.filter(event_date=today)
    categories = Category.objects.all()

    if type == "search":
        value = request.GET.get("search-value")
        if value:
            events = (
                events.filter(
                    models.Q(name__icontains=value)
                    | models.Q(location__icontains=value)
                )
                .annotate(
                    sort_group=Case(
                        When(event_date__gte=today, then=Value(0)),
                        When(event_date__lt=today, then=Value(1)),
                        output_field=IntegerField(),
                    ),
                    sort_date=Case(
                        When(
                            event_date__gte=today,
                            then=Extract("event_date", lookup_name="epoch"),
                        ),
                        When(
                            event_date__lt=today,
                            then=-Extract("event_date", lookup_name="epoch"),
                        ),
                        output_field=IntegerField(),
                    ),
                )
                .order_by("sort_group", "sort_date")
            )
    elif type == "category":
        id = request.GET.get("id")
        if id:
            events = (
                events.filter(category=id)
                .annotate(
                    sort_group=Case(
                        When(event_date__gte=today, then=Value(0)),
                        When(event_date__lt=today, then=Value(1)),
                        output_field=IntegerField(),
                    ),
                    sort_date=Case(
                        When(
                            event_date__gte=today,
                            then=Extract("event_date", lookup_name="epoch"),
                        ),
                        When(
                            event_date__lt=today,
                            then=-Extract("event_date", lookup_name="epoch"),
                        ),
                        output_field=IntegerField(),
                    ),
                )
                .order_by("sort_group", "sort_date")
            )
    elif type == "upcoming_events":
        events = events.filter(event_date__gt=today).order_by("event_date")
    elif type == "past_events":
        events = events.filter(event_date__lt=today).order_by("-event_date")
    elif type == "all_events":
        events = events.annotate(
            sort_group=Case(
                When(event_date__gte=today, then=Value(0)),
                When(event_date__lt=today, then=Value(1)),
                output_field=IntegerField(),
            ),
            sort_date=Case(
                When(
                    event_date__gte=today,
                    then=Extract("event_date", lookup_name="epoch"),
                ),
                When(
                    event_date__lt=today,
                    then=-Extract("event_date", lookup_name="epoch"),
                ),
                output_field=IntegerField(),
            ),
        ).order_by("sort_group", "sort_date")
    elif type == "date-range":
        date_from = request.GET.get("date-from")
        date_to = request.GET.get("date-to")
        events = (
            events.filter(event_date__gte=date_from, event_date__lte=date_to)
            .annotate(
                sort_group=Case(
                    When(event_date__gte=today, then=Value(0)),
                    When(event_date__lt=today, then=Value(1)),
                    output_field=IntegerField(),
                ),
                sort_date=Case(
                    When(
                        event_date__gte=today,
                        then=Extract("event_date", lookup_name="epoch"),
                    ),
                    When(
                        event_date__lt=today,
                        then=-Extract("event_date", lookup_name="epoch"),
                    ),
                    output_field=IntegerField(),
                ),
            )
            .order_by("sort_group", "sort_date")
        )

    context = {
        "count": counts,
        "events": events,
        "today": todayEvents,
        "categories": categories,
    }
    return render(request, "dashboard/organizer-dashboard.html", context)


def view_all(request):
    return render(request, "view-all.html", {"view_name": "Event"})
