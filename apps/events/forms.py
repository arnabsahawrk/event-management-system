from django import forms
from apps.core.helpers import StyledFormMixin
from .models import Event, Participant, Category
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile


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
            "image",
        ]
        widgets = {
            "description": forms.Textarea,
            "event_date": forms.DateInput(attrs={"type": "date"}),
            "event_time": forms.TimeInput(attrs={"type": "time"}),
            "category": forms.Select,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].required = False

    def clean_image(self):
        image = self.cleaned_data.get("image")

        if not image:
            if self.instance and self.instance.pk:
                return self.instance.image
            return None

        if isinstance(image, str):
            return image

        if isinstance(image, UploadedFile):
            max_size = 100 * 1024

            if image.size > max_size:
                raise ValidationError("Image size must be 100KB or less.")

            valid_mime_types = ["image/jpeg", "image/png", "image/webp", "image/jpg"]
            if image.content_type not in valid_mime_types:
                raise ValidationError("Only JPG, PNG, or WEBP images are allowed.")

            return image

        return None


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
