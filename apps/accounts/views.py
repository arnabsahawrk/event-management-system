from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from apps.accounts.forms import CreateGroupForm, CustomRegistrationForm, LoginForm
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
            return redirect("events:dashboard")
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


@login_required
def group_list(request):
    groups = Group.objects.prefetch_related("permissions").all()
    return render(
        request, "admin/view/group-list.html", {"groups": groups, "title": "Group List"}
    )


@login_required
def create_group(request):
    if request.method == "POST":
        group_form = CreateGroupForm(request.POST)

        if group_form.is_valid():
            group = group_form.save()
            messages.success(
                request, f"Group {group.name} has been created successfully"
            )
            return redirect("accounts:group-list")
        else:
            messages.error(request, "Something went wrong, please try again.")
            return redirect("accounts:create-group")
    else:
        group_form = CreateGroupForm()

    return render(
        request,
        "admin/form/create-group.html",
        {"group_form": group_form, "title": "Create Group"},
    )


def update_group(request, id):
    group = get_object_or_404(Group, id=id)

    if request.method == "POST":
        group_form = CreateGroupForm(request.POST, instance=group)

        if group_form.is_valid():
            group_form.save()
            messages.success(request, "Group updated successfully")
            return redirect(f"{reverse('accounts:update-group', args=[id])}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        group_form = CreateGroupForm(instance=group)

    context = {"group_form": group_form, "title": "Update Group"}
    return render(request, "admin/form/create-group.html", context)


@login_required
def delete_group(request, id):
    if request.method == "POST":
        group = get_object_or_404(Group, id=id)
        group.delete()
        messages.success(request, "Group deleted successfully.")
    else:
        messages.error(request, "Something went wrong, try again.")

    return redirect("accounts:group-list")
