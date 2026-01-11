from typing import cast
from django.db import models
from django.db.models import Case, IntegerField, Value, When
from django.db.models.functions import Extract
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages

from apps.core.helpers import is_admin_or_organizer, is_participant
from apps.events.forms import CategoryModelForm, EventModelForm
from apps.events.models import RSVP, Category, Event
from django.views import View
from django.views.generic import ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class DashboardView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "dashboard.html"
    context_object_name = "events"

    def get_queryset(self):
        today = timezone.localdate()
        qs = Event.objects.select_related("category").all()

        filter_type = self.request.GET.get("type")

        def sorted_queryset(queryset):
            return queryset.annotate(
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

        if filter_type == "search":
            value = self.request.GET.get("search-value")
            if value:
                qs = qs.filter(
                    models.Q(name__icontains=value)
                    | models.Q(location__icontains=value)
                )
                qs = sorted_queryset(qs)

        elif filter_type == "category":
            category_id = self.request.GET.get("id")
            if category_id:
                qs = qs.filter(category=category_id)
                qs = sorted_queryset(qs)

        elif filter_type == "upcoming_events":
            qs = qs.filter(event_date__gt=today).order_by("event_date")

        elif filter_type == "past_events":
            qs = qs.filter(event_date__lt=today).order_by("-event_date")

        elif filter_type == "all_events":
            qs = sorted_queryset(qs)

        elif filter_type == "date-range":
            date_from = self.request.GET.get("date-from")
            date_to = self.request.GET.get("date-to")
            if date_from and date_to:
                qs = qs.filter(
                    event_date__gte=date_from,
                    event_date__lte=date_to,
                )
                qs = sorted_queryset(qs)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.localdate()

        context["count"] = Event.objects.aggregate(
            total_rsvps=models.Count("rsvps", distinct=True),
            total_events=models.Count("id", distinct=True),
            upcoming_events=models.Count(
                "id", filter=models.Q(event_date__gt=today), distinct=True
            ),
            past_events=models.Count(
                "id", filter=models.Q(event_date__lt=today), distinct=True
            ),
        )

        context["today"] = Event.objects.filter(event_date=today)
        context["categories"] = Category.objects.all()

        return context


class ViewAllView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return is_admin_or_organizer(self.request.user)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return redirect("core:no-permission")

    def get(self, request, *args, **kwargs):
        view_type = request.GET.get("type")

        if view_type == "category":
            categories = Category.objects.prefetch_related("events").annotate(
                events_count=models.Count("events", distinct=True)
            )
            context = {
                "title": "Category",
                "categories": categories,
            }
            return render(request, "view/category-view.html", context)

        events = Event.objects.select_related("category").all()
        context = {
            "title": "Event",
            "events": events,
        }
        return render(request, "view/event-view.html", context)


class CreateFormView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return is_admin_or_organizer(self.request.user)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return redirect("core:no-permission")

    def get(self, request, *args, **kwargs):
        form_type = request.GET.get("type")

        if form_type == "category":
            form = CategoryModelForm()
            return render(
                request,
                "form/create-category.html",
                {"title": "Create Category", "category_form": form},
            )

        form = EventModelForm()
        return render(
            request,
            "form/create-event.html",
            {"title": "Create Event", "event_form": form},
        )

    def post(self, request, *args, **kwargs):
        form_type = request.GET.get("type")

        if form_type == "category":
            form = CategoryModelForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Category created successfully")
                return redirect(f"{reverse('events:view-all')}?type=category")

            messages.error(request, "Please correct the errors below.")
            return render(
                request,
                "form/create-category.html",
                {"title": "Create Category", "category_form": form},
            )

        form = EventModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event created successfully")
            return redirect(f"{reverse('events:view-all')}?type=event")

        messages.error(request, "Please correct the errors below.")
        return render(
            request,
            "form/create-event.html",
            {"title": "Create Event", "event_form": form},
        )


class UpdateFormView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return is_admin_or_organizer(self.request.user)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return redirect("core:no-permission")

    def get(self, request, id, *args, **kwargs):
        form_type = request.GET.get("type")

        if form_type == "category":
            category = get_object_or_404(Category, id=id)
            form = CategoryModelForm(instance=category)
            return render(
                request,
                "form/create-category.html",
                {"title": "Update Category", "category_form": form},
            )

        event = get_object_or_404(Event, id=id)
        form = EventModelForm(instance=event)
        return render(
            request,
            "form/create-event.html",
            {"title": "Update Event", "event_form": form},
        )

    def post(self, request, id, *args, **kwargs):
        form_type = request.GET.get("type")

        if form_type == "category":
            category = get_object_or_404(Category, id=id)
            form = CategoryModelForm(request.POST, instance=category)

            if form.is_valid():
                form.save()
                messages.success(request, "Category updated successfully")
                return redirect(
                    f"{reverse('events:update-form', args=[id])}?type=category"
                )

            messages.error(request, "Please correct the errors below.")
            return render(
                request,
                "form/create-category.html",
                {"title": "Update Category", "category_form": form},
            )

        event = get_object_or_404(Event, id=id)
        form = EventModelForm(request.POST, request.FILES, instance=event)

        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully")
            return redirect(f"{reverse('events:update-form', args=[id])}?type=event")

        messages.error(request, "Please correct the errors below.")
        return render(
            request,
            "form/create-event.html",
            {"title": "Update Event", "event_form": form},
        )


class DeleteFormView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return is_admin_or_organizer(self.request.user)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return redirect("core:no-permission")

    def post(self, request, id, *args, **kwargs):
        form_type = request.GET.get("type")

        if form_type == "category":
            category = get_object_or_404(Category, id=id)
            category.delete()
            messages.success(request, "Category deleted successfully")
            return redirect(f"{reverse('events:view-all')}?type=category")

        event = get_object_or_404(Event, id=id)
        event.delete()
        messages.success(request, "Event deleted successfully")
        return redirect(f"{reverse('events:view-all')}?type=event")


class RSVPView(LoginRequiredMixin, UserPassesTestMixin, ListView):

    model = RSVP
    template_name = "view/rsvp-view.html"
    context_object_name = "rsvps"

    def test_func(self):
        return is_participant(self.request.user)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return redirect("core:no-permission")

    def get_queryset(self):
        today = timezone.localdate()

        return (
            RSVP.objects.select_related("event")
            .filter(user=self.request.user)
            .annotate(
                sort_group=Case(
                    When(event__event_date__gte=today, then=Value(0)),
                    When(event__event_date__lt=today, then=Value(1)),
                    output_field=IntegerField(),
                ),
                sort_date=Case(
                    When(
                        event__event_date__gte=today,
                        then=Extract("event__event_date", "epoch"),
                    ),
                    When(
                        event__event_date__lt=today,
                        then=-Extract("event__event_date", "epoch"),
                    ),
                    output_field=IntegerField(),
                ),
            )
            .order_by("sort_group", "sort_date")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "RSVP"
        return context


class RSVPEventView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return is_participant(self.request.user)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return redirect("core:no-permission")

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)

        if event.day_status == "Past":
            messages.info(request, "This event has passed away.")
            return redirect("events:rsvp-view")

        if not request.user.groups.filter(name="Participant").exists():
            messages.error(request, "Only participants can RSVP for events.")
            return redirect("events:dashboard")

        rsvp, created = RSVP.objects.get_or_create(
            user=request.user,
            event=event,
        )

        if created:
            messages.success(
                request,
                f"RSVP confirmed for {event.name}! An invitation email has been sent.",
            )
        else:
            messages.info(request, f"You have already RSVPed for {event.name}.")

        return redirect("events:rsvp-view")


class RSVPDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = RSVP
    pk_url_kwarg = "id"

    def test_func(self):
        return is_participant(self.request.user)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return redirect("core:no-permission")

    def get(self, request, *args, **kwargs):
        messages.error(request, "Invalid request.")
        return redirect("events:rsvp-view")

    def post(self, request, *args, **kwargs):
        rsvp = cast(RSVP, self.get_object())

        if rsvp.event.day_status == "Past":
            messages.error(request, "You cannot cancel an RSVP for a past event.")
            return redirect("events:rsvp-view")

        try:
            rsvp.delete()
            messages.success(request, "RSVP canceled successfully.")
        except Exception:
            messages.error(
                request,
                "Something went wrong. Please try again.",
            )
        return redirect("events:rsvp-view")
