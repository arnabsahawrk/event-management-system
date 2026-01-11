from django import template
from django.utils import timezone

register = template.Library()


@register.filter(name="custom_datetime")
def custom_datetime(value):
    if not value:
        return "No record available"

    value = timezone.localtime(value)
    today = timezone.localdate()
    value_date = value.date()

    if value_date == today:
        return f"Today at {value.strftime('%I:%M %p')}"
    elif value_date == today - timezone.timedelta(days=1):
        return f"Yesterday at {value.strftime('%I:%M %p')}"
    else:
        return f"{value.strftime('%B %d, %I:%M %p')}"
