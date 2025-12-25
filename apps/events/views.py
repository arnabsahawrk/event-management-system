from django.db import models
from django.db.models import Case, IntegerField, Value, When
from django.db.models.functions import Extract
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages

from apps.events.forms import CategoryModelForm, EventModelForm, ParticipantModelForm
from apps.events.models import RSVP, Category, Event, Participant
from django.contrib.auth.decorators import login_required


def dashboard(request):
    today = timezone.now().date()

    type = request.GET.get("type")

    counts = Event.objects.aggregate(
        total_rsvps=models.Count("rsvps", distinct=True),
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
    return render(request, "dashboard.html", context)


def view_all(request):
    type = request.GET.get("type")

    if type == "participant":
        participants = Participant.objects.prefetch_related("events").annotate(
            events_count=models.Count("events", distinct=True)
        )
        context = {"title": "Participant", "participants": participants}
        return render(request, "view/participant-view.html", context)
    elif type == "category":
        categories = Category.objects.prefetch_related("events").annotate(
            events_count=models.Count("events", distinct=True)
        )
        context = {"title": "Category", "categories": categories}
        return render(request, "view/category-view.html", context)
    else:
        events = Event.objects.select_related("category").all()
        context = {"title": "Event", "events": events}
        return render(request, "view/event-view.html", context)


def create_form(request):
    type = request.GET.get("type")

    if type == "participant":
        if request.method == "POST":
            participant_form = ParticipantModelForm(request.POST)

            if participant_form.is_valid():
                participant_form.save()
                messages.success(request, "Participant created successfully")
                return redirect(f"{reverse('events:view-all')}?type=participant")

            messages.error(request, "Please correct the errors below.")
        else:
            participant_form = ParticipantModelForm()

        context = {"title": "Create Participant", "participant_form": participant_form}
        return render(request, "form/create-participant.html", context)
    elif type == "category":
        if request.method == "POST":
            category_form = CategoryModelForm(request.POST)

            if category_form.is_valid():
                category_form.save()
                messages.success(request, "Category created successfully")
                return redirect(f"{reverse('events:view-all')}?type=category")

            messages.error(request, "Please correct the errors below.")
        else:
            category_form = CategoryModelForm()

        context = {"title": "Create Category", "category_form": category_form}
        return render(request, "form/create-category.html", context)
    else:
        if request.method == "POST":
            event_form = EventModelForm(request.POST, request.FILES)

            if event_form.is_valid():
                event_form.save()
                messages.success(request, "Event created successfully")
                return redirect(f"{reverse('events:view-all')}?type=event")

            messages.error(request, "Please correct the errors below.")
        else:
            event_form = EventModelForm()

        context = {"title": "Create Event", "event_form": event_form}
        return render(request, "form/create-event.html", context)


def update_form(request, id):
    type = request.GET.get("type")

    if type == "participant":
        participant = Participant.objects.get(id=id)

        if request.method == "POST":
            participant_form = ParticipantModelForm(request.POST, instance=participant)

            if participant_form.is_valid():
                participant_form.save()
                messages.success(request, "Participant updated successfully")
                return redirect(
                    f"{reverse('events:update-form', args=[id])}?type=participant"
                )
            messages.error(request, "Please correct the errors below.")
        else:
            participant_form = ParticipantModelForm(instance=participant)

        context = {"title": "Update Participant", "participant_form": participant_form}
        return render(request, "form/create-participant.html", context)

    elif type == "category":
        category = Category.objects.get(id=id)

        if request.method == "POST":
            category_form = CategoryModelForm(request.POST, instance=category)

            if category_form.is_valid():
                category_form.save()
                messages.success(request, "Category updated successfully")
                return redirect(
                    f"{reverse('events:update-form', args=[id])}?type=category"
                )
            messages.error(request, "Please correct the errors below.")
        else:
            category_form = CategoryModelForm(instance=category)

        context = {"title": "Update Category", "category_form": category_form}
        return render(request, "form/create-category.html", context)

    else:
        event = Event.objects.get(id=id)

        if request.method == "POST":
            event_form = EventModelForm(request.POST, request.FILES, instance=event)

            if event_form.is_valid():
                event_form.save()
                messages.success(request, "Event updated successfully")
                return redirect(
                    f"{reverse('events:update-form', args=[id])}?type=event"
                )
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            event_form = EventModelForm(instance=event)

        context = {"title": "Update Event", "event_form": event_form}
        return render(request, "form/create-event.html", context)


def delete(request, id):
    type = request.GET.get("type")

    if type == "participant":
        if request.method == "POST":
            participant = Participant.objects.get(id=id)
            participant.delete()
            messages.success(request, "Participant deleted successfully")
            return redirect(f"{reverse('events:view-all')}?type=participant")
        else:
            messages.error(request, "Something went wrong, try again.")
            return redirect(f"{reverse('events:view-all')}?type=participant")
    elif type == "category":
        if request.method == "POST":
            category = Category.objects.get(id=id)
            category.delete()
            messages.success(request, "Category deleted successfully")
            return redirect(f"{reverse('events:view-all')}?type=category")
        else:
            messages.error(request, "Something went wrong, try again.")
            return redirect(f"{reverse('events:view-all')}?type=category")
    else:
        if request.method == "POST":
            event = Event.objects.get(id=id)
            event.delete()
            messages.success(request, "Event deleted successfully")
            return redirect(f"{reverse('events:view-all')}?type=event")
        else:
            messages.error(request, "Something went wrong. try again.")
            return redirect(f"{reverse('events:view-all')}?type=event")


@login_required
def rsvp_view(request):
    today = timezone.now().date()

    rsvps = (
        RSVP.objects.select_related("event")
        .filter(user=request.user)
        .annotate(
            sort_group=Case(
                When(event__event_date__gte=today, then=Value(0)),
                When(event__event_date__lt=today, then=Value(1)),
                output_field=IntegerField(),
            ),
            sort_date=Case(
                When(
                    event__event_date__gte=today,
                    then=Extract("event__event_date", lookup_name="epoch"),
                ),
                When(
                    event__event_date__lt=today,
                    then=-Extract("event__event_date", lookup_name="epoch"),
                ),
                output_field=IntegerField(),
            ),
        )
        .order_by("sort_group", "sort_date")
    )

    context = {
        "title": "RSVP",
        "rsvps": rsvps,
    }
    return render(request, "view/rsvp-view.html", context)


@login_required
def rsvp_events(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.day_status == "Past":
        messages.info(request, "This event has passed away.")
    elif request.method == "POST":
        rsvp, created = RSVP.objects.get_or_create(user=request.user, event=event)

        if created:
            messages.success(
                request,
                f"RSVP confirmed for {event.name}! A confirmation email has been sent to your mail address.",
            )
        else:
            messages.info(request, f"You have already RSVPed for {event.name}.")
    else:
        messages.error(request, "Something went wrong. try again.")

    return redirect("events:rsvp-view")


@login_required
def rsvp_delete(request, id):
    if request.method == "POST":
        rsvp = RSVP.objects.get(id=id)

        rsvp.delete()
        messages.success(request, "RSVP canceled successfully.")
    else:
        messages.error(request, "Something went wrong. try again.")

    return redirect("events:rsvp-view")
