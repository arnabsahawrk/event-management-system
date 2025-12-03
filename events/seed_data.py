from events.models import Event, Participant, Category
from datetime import time, date


def seed_database():
    if Category.objects.exists():
        return "Data already exists! Seeder skipped."

    # 1. CATEGORIES
    categories = [
        ("Technology", "Events related to tech, software, and gadgets"),
        ("Business", "Business conferences, meetups, and networking"),
        ("Education", "Workshops, study sessions, and learning events"),
        ("Health", "Wellness, medical, and fitness programs"),
        ("Sports", "Sporting events and activities"),
        ("Music", "Concerts, bands, and musical nights"),
        ("Arts", "Arts and crafts exhibitions"),
        ("Travel", "Trips, tours and outdoor adventure"),
        ("Food", "Food festivals and cooking shows"),
        ("Community", "Local community gatherings"),
        ("Charity", "Donation drives and charity events"),
        ("Startup", "Startup events and pitch competitions"),
        ("Marketing", "Marketing, branding workshops"),
        ("Gaming", "Esports gaming tournaments"),
        ("Photography", "Photo walks and exhibitions"),
    ]

    category_objs = []
    for name, desc in categories:
        category_objs.append(Category.objects.create(name=name, description=desc))

    # 2. EVENTS (just 10 events to keep it small)
    events = [
        (
            "Tech Expo 2025",
            "New tech products showcase",
            date(2025, 12, 20),
            time(10, 0),
            "Dhaka Expo Center",
            0,
        ),
        (
            "Business Meetup",
            "Monthly networking meetup",
            date(2025, 12, 10),
            time(18, 0),
            "Banani Convention",
            1,
        ),
        (
            "Photography Walk",
            "City photo walk",
            date(2025, 12, 30),
            time(8, 0),
            "Old Dhaka",
            14,
        ),
        ("Food Carnival", "Food fair", date(2025, 12, 9), time(12, 0), "Hatirjheel", 8),
        (
            "Startup Demo Day",
            "Pitching event",
            date(2025, 12, 28),
            time(11, 0),
            "Mohakhali Hub",
            11,
        ),
        (
            "Yoga Wellness Camp",
            "Health and wellness",
            date(2025, 12, 22),
            time(7, 30),
            "Dhanmondi Park",
            3,
        ),
        (
            "Football Tournament",
            "Sports championship",
            date(2025, 12, 15),
            time(16, 0),
            "Mirpur Stadium",
            4,
        ),
        (
            "Rock Music Night",
            "Live rock concert",
            date(2025, 12, 17),
            time(19, 0),
            "Gulshan Club",
            5,
        ),
        (
            "Art & Craft Fair",
            "Art exhibition",
            date(2025, 12, 14),
            time(14, 0),
            "Shilpakala Academy",
            6,
        ),
    ]

    event_objs = []
    for name, desc, e_date, e_time, loc, cat_index in events:
        event_objs.append(
            Event.objects.create(
                name=name,
                description=desc,
                event_date=e_date,
                event_time=e_time,
                location=loc,
                category=category_objs[cat_index],
            )
        )

    # 3. PARTICIPANTS (20 sample people)
    participants = [
        "Arnab Saha",
        "Rahim Uddin",
        "Karina Rahman",
        "Fahim Ahmed",
        "Sadia Hasan",
        "Imran Khan",
        "Nusrat Jahan",
        "Jamil Chowdhury",
        "Sara Islam",
        "Hasib Karim",
        "Rafiul Hasan",
        "Omar Sadat",
        "Jannat Akter",
        "Tanvir Ahmed",
        "Afsana Mim",
        "Shakib Hasan",
        "Priya Sen",
        "Rifat Mahmud",
        "Tahsin Nabil",
        "Fatima Akter",
    ]

    participant_objs = []
    email_count = 1
    for name in participants:
        participant_objs.append(
            Participant.objects.create(
                name=name, email=f"user{email_count}@example.com"
            )
        )
        email_count += 1

    # Assign participants randomly to events
    for p in participant_objs:
        p.events.add(event_objs[email_count % len(event_objs)])
        email_count += 1

    return "Database successfully seeded!"
