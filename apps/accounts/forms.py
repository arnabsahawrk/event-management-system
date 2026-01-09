from django import forms
from django.contrib.auth.models import Group, Permission
import re
from apps.accounts.models import CustomUser
from apps.core.helpers import StyledFormMixin
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomRegistrationForm(StyledFormMixin, forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        labels = {
            "username": "Username",
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email",
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        errors = []

        if not password:
            raise forms.ValidationError("Password is required")

        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")

        if not re.search(r"[A-Z]", password):
            errors.append("Password must contain at least one uppercase letter")

        if not re.search(r"[a-z]", password):
            errors.append("Password must contain at least one lowercase letter")

        if not re.search(r"[0-9]", password):
            errors.append("Password must contain at least one digit")

        if not re.search(r"[@#$%^&+=]", password):
            errors.append("Password must contain at least one special character")

        if errors:
            raise forms.ValidationError(errors)

        return password

    def clean_email(self):
        email = self.cleaned_data.get("email")
        email_exits = User.objects.filter(email=email).exists()

        if email_exits:
            raise forms.ValidationError("Email already exits")

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data


class LoginForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CreateGroupForm(StyledFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assign Permission",
    )

    class Meta:
        model = Group
        fields = ["name", "permissions"]


class AssignRoleForm(forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select role",
        widget=forms.Select(
            attrs={
                "class": (
                    "px-2 py-1 border border-gray-300 rounded-md text-sm "
                    "focus:outline-none focus:ring-1 focus:ring-blue-500 "
                    "bg-white"
                )
            }
        ),
    )


class EditUserProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "phone_number", "profile_image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["profile_image"].required = False
        self.fields["phone_number"].required = False

    def clean_profile_image(self):
        image = self.cleaned_data.get("profile_image")

        if image is False:
            return "profile/default.jpg"

        if not image:
            if self.instance and self.instance.pk:
                return self.instance.profile_image
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

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")

        if not phone:
            return phone

        phone = phone.strip()

        if not phone.isdigit():
            raise ValidationError("Phone number must contain only digits.")

        if len(phone) != 11:
            raise ValidationError("Phone number must be exactly 11 digits.")

        if not phone.startswith("01"):
            raise ValidationError("Phone number must start with 01.")

        return phone
