from django import forms
from apps.core.helpers import StyledFormMixin
from .models import Event, Participant, Category


class EventModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "name",
            "description",
            "event_date",
            "event_time",
            "location",
            "category",
        ]
        widgets = {
            "description": forms.Textarea,
            "event_date": forms.DateInput(attrs={"type": "date"}),
            "event_time": forms.TimeInput(attrs={"type": "time"}),
            "category": forms.Select,
        }


class ParticipantModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Participant
        fields = ["name", "email", "events"]
        widgets = {
            "events": forms.CheckboxSelectMultiple,
            "email": forms.EmailInput,
        }


class CategoryModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]
        widgets = {"description": forms.Textarea}
