from django.shortcuts import redirect, render
from apps.accounts.forms import CustomRegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


def register(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    if request.method == "POST":
        register_form = CustomRegistrationForm(request.POST)

        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.set_password(register_form.cleaned_data["password"])
            user.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect("accounts:login")
        messages.error(request, "Please correct the errors below.")
    else:
        register_form = CustomRegistrationForm()

    return render(request, "register.html", {"register_form": register_form})


def login(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    if request.method == "POST":
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            auth_login(request, user)
            return redirect("core:home")
        messages.error(request, "Please correct the errors below.")
    else:
        login_form = LoginForm()

    return render(request, "login.html", {"login_form": login_form})


@login_required
def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect("accounts:login")
    else:
        return redirect("core:home")


def group_list(request):
    groups = Group.objects.prefetch_related("permissions").all()
    return render(
        request, "admin/view/group-list.html", {"groups": groups, "title": "Group List"}
    )
