from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group


@receiver(post_save, sender=User)
def assign_default_role(sender, instance, created, **kwargs):

    if created:
        participant_group, was_created = Group.objects.get_or_create(name="Participant")

        instance.groups.add(participant_group)

        if was_created:
            print("Created new group: Participant")
        print(f"User {instance.username} assigned to Participant group")
