import os
import random
from datetime import datetime, timedelta

import django
from django.utils import timezone
from faker import Faker

from apps.events.models import Category, Event, Participant

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


fake = Faker()


def populate_db(
    num_categories=7,
    num_events=80,
    num_participants=100,
    max_participants_per_event=30,
):

    print("Clearing old data...")
    Category.objects.all().delete()
    Event.objects.all().delete()
    Participant.objects.all().delete()

    print("Creating categories...")
    categories = []
    for _ in range(num_categories):
        categories.append(
            Category(
                name=fake.word().title(),
                description=fake.sentence(),
            )
        )
    Category.objects.bulk_create(categories)
    categories = list(Category.objects.all())

    print("Creating events...")
    events = []
    today = timezone.now().date()

    for _ in range(num_events):
        delta_days = random.randint(-30, 30)
        date = today + timedelta(days=delta_days)
        hour = random.randint(8, 20)

        events.append(
            Event(
                name=fake.sentence(nb_words=5)[:250],
                description=fake.paragraph(nb_sentences=3),
                event_date=date,
                event_time=datetime.strptime(f"{hour}:00", "%H:%M").time(),
                location=fake.city(),
                category=random.choice(categories),
            )
        )

    Event.objects.bulk_create(events)
    events = list(Event.objects.all())

    print("Creating participants...")
    participants = []
    fake.unique.clear()

    for _ in range(num_participants):
        participants.append(
            Participant(
                name=fake.name(),
                email=fake.unique.email(),
            )
        )

    Participant.objects.bulk_create(participants)
    participants = list(Participant.objects.all())

    print("Assigning participants to events...")
    for event in events:
        count = random.randint(5, max_participants_per_event)
        selected = random.sample(participants, count)
        event.participants.add(*selected)  # type: ignore

    print("Done! Database populated successfully.")


if __name__ == "__main__":
    populate_db()
