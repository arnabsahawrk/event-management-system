from django import forms
from django.forms import (
    TextInput,
    EmailInput,
    PasswordInput,
    Textarea,
    Select,
    SelectMultiple,
    CheckboxSelectMultiple,
    DateInput,
    TimeInput,
    ClearableFileInput,
)
from typing import TYPE_CHECKING


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

    if TYPE_CHECKING:
        fields: dict[str, forms.Field]

    default_classes = (
        "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm "
        "focus:outline-none focus:border-rose-500 focus:ring-rose-500"
    )

    def apply_styled_widgets(self):
        for name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, (TextInput, EmailInput, PasswordInput)):
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
                        "class": (
                            "border-2 border-gray-300 p-3 rounded-lg shadow-sm "
                            "focus:outline-none focus:border-rose-500 focus:ring-rose-500 w-full"
                        ),
                    }
                )

            elif isinstance(widget, (SelectMultiple, CheckboxSelectMultiple)):
                widget.attrs.update(
                    {
                        "class": (
                            "space-y-2"
                            if isinstance(widget, CheckboxSelectMultiple)
                            else "w-full p-2 rounded-lg border border-gray-300"
                        )
                    }
                )

            elif isinstance(widget, (DateInput, TimeInput)):
                widget.attrs.update(
                    {
                        "class": "border-2 border-gray-300 p-2 rounded-lg shadow-sm focus:outline-none"
                    }
                )

            elif isinstance(widget, ClearableFileInput):
                widget.attrs.update(
                    {
                        "class": (
                            "block w-full text-sm text-gray-700 "
                            "file:mr-4 file:py-2 file:px-4 "
                            "file:rounded-lg file:border-0 "
                            "file:text-sm file:font-medium "
                            "file:bg-blue-50 file:text-blue-700 "
                            "hover:file:bg-blue-100"
                        ),
                        "accept": "image/*",
                    }
                )

            else:
                existing = widget.attrs.get("class", "")
                widget.attrs.update(
                    {"class": f"{existing} {self.default_classes}".strip()}
                )
