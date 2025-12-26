from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings
from .models import RSVP


@receiver(post_save, sender=RSVP)
def send_rsvp_confirmation_email(sender, instance, created, **kwargs):
    if created:
        subject = f"RSVP Confirmed for {instance.event.name}"
        message = f"""
        Hi {instance.user.username},

        Your RSVP for the event "{instance.event.name}" has been confirmed!

        Event Details:
        - Name: {instance.event.name}
        - Date: {instance.event.event_date}
        - Location: {instance.event.location}
        - Description: {instance.event.description}

        Thank you for participating!

        Best regards,
        Arnab Saha
        """

        recipient_list = [instance.user.email]

        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        except Exception as e:
            print(
                f"Failed to send RSVP confirmation email to {instance.user.email}: {str(e)}"
            )
