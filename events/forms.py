from django import forms
from typing import TYPE_CHECKING
from django.forms.widgets import (
    TextInput,
    Textarea,
    Select,
    SelectMultiple,
    CheckboxSelectMultiple,
    DateInput,
    TimeInput,
    EmailInput,
)
from .models import Event, Participant, Category


class StyledFormMixin:
    if TYPE_CHECKING:
        fields: dict[str, forms.Field]

    default_classes = (
        "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm "
        "focus:outline-none focus:border-rose-500 focus:ring-rose-500"
    )

    def apply_styled_widgets(self):
        for name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, (TextInput, EmailInput)):
                widget.attrs.update(
                    {
                        "class": self.default_classes,
                        "placeholder": widget.attrs.get(
                            "placeholder", f"Enter {field.label}"
                        ),
                    }
                )
            elif isinstance(widget, Textarea):
                widget.attrs.update(
                    {
                        "class": self.default_classes,
                        "placeholder": widget.attrs.get(
                            "placeholder", f"Enter {field.label}"
                        ),
                        "rows": widget.attrs.get("rows", 4),
                    }
                )
            elif isinstance(widget, Select):
                widget.attrs.update(
                    {
                        "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none "
                        "focus:border-rose-500 focus:ring-rose-500 w-full",
                    }
                )
            elif isinstance(widget, (SelectMultiple, CheckboxSelectMultiple)):
                if isinstance(widget, CheckboxSelectMultiple):
                    widget.attrs.update({"class": "space-y-2"})
                else:
                    widget.attrs.update(
                        {"class": "w-full p-2 rounded-lg border border-gray-300"}
                    )
            elif isinstance(widget, (DateInput, TimeInput)):
                widget.attrs.update(
                    {
                        "class": "border-2 border-gray-300 p-2 rounded-lg shadow-sm focus:outline-none"
                    }
                )
            else:
                existing = widget.attrs.get("class", "")
                if "border-2" not in existing:
                    widget.attrs.update(
                        {"class": f"{existing} {self.default_classes}".strip()}
                    )


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()


class ParticipantModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Participant
        fields = ["name", "email", "events"]
        widgets = {
            "events": forms.CheckboxSelectMultiple,
            "email": forms.EmailInput,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()


class CategoryModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]
        widgets = {"description": forms.Textarea}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()
