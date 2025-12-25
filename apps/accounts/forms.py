from django import forms
from django.contrib.auth.models import User, Group, Permission
import re
from apps.core.helpers import StyledFormMixin
from django.contrib.auth.forms import AuthenticationForm


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
