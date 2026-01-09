from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from apps.accounts.forms import (
    AssignRoleForm,
    ChangeUserPasswordForm,
    CreateGroupForm,
    CustomRegistrationForm,
    EditUserProfileForm,
    LoginForm,
)
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group

from apps.accounts.models import CustomUser
from apps.core.helpers import is_admin
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import UpdateView, CreateView
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

User = get_user_model()


def register(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    if request.method == "POST":
        register_form = CustomRegistrationForm(request.POST)

        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.set_password(register_form.cleaned_data["password"])
            user.is_active = False
            user.save()
            messages.success(
                request,
                "Registration successful. Please activate your account and log in to continue.",
            )
            return redirect("accounts:login")
        messages.error(request, "Please correct the errors below.")
    else:
        register_form = CustomRegistrationForm()

    return render(request, "register.html", {"register_form": register_form})


class RegisterView(CreateView):
    pass


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


class UserProfileView(LoginRequiredMixin, TemplateView):
    login_url = "accounts:login"
    template_name = "profile/overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "profile"
        return context


class EditUserProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = EditUserProfileForm
    template_name = "profile/edit.html"
    login_url = "accounts:login"
    success_url = reverse_lazy("accounts:overview")

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "edit"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class ChangeUserPasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = ChangeUserPasswordForm
    template_name = "profile/password.html"
    login_url = "accounts:login"
    success_url = reverse_lazy("accounts:password")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "password"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Your password has been updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


@login_required
@user_passes_test(is_admin, login_url="core:no-permission")
def group_list(request):
    groups = Group.objects.prefetch_related("permissions").all()
    return render(
        request, "admin/view/group-list.html", {"groups": groups, "title": "Group List"}
    )


@login_required
@user_passes_test(is_admin, login_url="core:no-permission")
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


@login_required
@user_passes_test(is_admin, login_url="core:no-permission")
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
@user_passes_test(is_admin, login_url="core:no-permission")
def delete_group(request, id):
    if request.method == "POST":
        group = get_object_or_404(Group, id=id)

        if (
            group.name == "Admin"
            or group.name == "Organizer"
            or group.name == "Participant"
        ):
            messages.error(
                request,
                "You cannot delete a default group. Default groups are: Admin, Organizer, Participant.",
            )
            return redirect("accounts:group-list")

        group.delete()
        messages.success(request, "Group deleted successfully.")
    else:
        messages.error(request, "Something went wrong, try again.")

    return redirect("accounts:group-list")


@login_required
@user_passes_test(is_admin, login_url="core:no-permission")
def user_list(request):
    users = User.objects.prefetch_related("groups").order_by("-date_joined")
    assign_form = AssignRoleForm()

    context = {"title": "All Users", "users": users, "assign_form": assign_form}
    return render(request, "admin/view/user-list.html", context)


@login_required
@user_passes_test(is_admin, login_url="core:no-permission")
def assign_role(request, user_id):
    if request.user.id == user_id:
        messages.error(request, "You cannot assign a role to yourself.")
        return redirect("accounts:user-list")

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data["role"]
            user.groups.clear()
            user.groups.add(role)

            messages.success(
                request,
                f"User {user.username} has been assigned to the {role.name} role",
            )
            return redirect("accounts:user-list")

    messages.error(request, "Something went wrong, please try again.")
    return redirect("accounts:user-list")


@login_required
@user_passes_test(is_admin, login_url="core:no-permission")
def delete_user(request, user_id):
    if request.user.id == user_id:
        messages.error(request, "You cannot delete yourself.")
        return redirect("accounts:user-list")

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect("accounts:user-list")

    messages.error(request, "Something went wrong, please try again.")
    return redirect("accounts:user-list")


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(
                request,
                "Your account has been activated successfully. You can now log in.",
            )
            return redirect("accounts:login")
        else:
            return HttpResponse("Invalid Id or Token")
    except User.DoesNotExist:
        return HttpResponse("User not found")
