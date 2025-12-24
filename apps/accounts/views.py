from django.shortcuts import redirect, render
from apps.accounts.forms import CustomRegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        register_form = CustomRegistrationForm(request.POST)

        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.set_password(register_form.cleaned_data["password"])
            user.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")

    register_form = CustomRegistrationForm()
    return render(request, "register.html", {"register_form": register_form})


def login(request):
    if request.user.is_authenticated:
        return redirect("home")

    login_form = LoginForm()
    if request.method == "POST":
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            auth_login(request, user)
            return redirect("home")

    return render(request, "login.html", {"login_form": login_form})


def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect("login")
    else:
        return redirect("home")
