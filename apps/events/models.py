from django.db import models
from django.utils import timezone


class Event(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    event_date = models.DateField()
    event_time = models.TimeField()
    location = models.CharField(max_length=100)

    image = models.ImageField(
        upload_to="events/", default="events/default.jpg", blank=True, null=True
    )

    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, related_name="events"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    @property
    def day_status(self):
        today = timezone.now().date()

        if self.event_date == today:
            return "Today"
        elif self.event_date > today:
            return "Upcoming"
        else:
            return "Past"

    def __str__(self) -> str:
        return self.name


class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    events = models.ManyToManyField(Event, related_name="participants")

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name
