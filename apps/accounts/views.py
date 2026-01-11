from typing import cast
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from apps.accounts.forms import (
    AssignRoleForm,
    ChangeUserPasswordForm,
    CreateGroupForm,
    CustomRegistrationForm,
    EditUserProfileForm,
    ForgotPasswordForm,
    LoginForm,
    ForgotPasswordConfirmForm,
)
from django.contrib import messages
from django.contrib.auth.models import Group
from apps.accounts.models import CustomUser
from apps.core.helpers import is_admin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    TemplateView,
    UpdateView,
    CreateView,
    ListView,
    DeleteView,
)
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
)
from django.urls import reverse_lazy
from django.views import View

User = get_user_model()


class RegisterView(CreateView):
    model = User
    form_class = CustomRegistrationForm
    template_name = "register.html"
    success_url = reverse_lazy("accounts:login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("core:home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.is_active = False
        user.save()
        messages.success(
            self.request,
            "Registration successful! Please check your email to activate your account.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = "login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("core:home")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        return next_url or super().get_success_url()


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("core:home")
        return super().dispatch(request, *args, **kwargs)


class ActiveUserView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("core:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_id, token):
        try:
            user = get_object_or_404(User, id=user_id)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()

                messages.success(
                    request,
                    "Your account has been activated successfully! You can now log in.",
                )
                return redirect("accounts:login")
            else:
                messages.error(
                    request, "Invalid activation link. Please request a new one."
                )
                return redirect("accounts:login")
        except Exception as e:
            print(e)
            messages.error(
                request,
                "An error occurred during activation. Please try again.",
            )
            return redirect("accounts:login")


class ForgotPasswordView(PasswordResetView):
    form_class = ForgotPasswordForm
    template_name = "reset-password.html"
    success_url = reverse_lazy("accounts:login")
    email_template_name = "reset-email.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("core:home")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["protocol"] = "https" if self.request.is_secure() else "http"
        context["domain"] = self.request.get_host()
        return context

    def form_valid(self, form):
        messages.success(
            self.request, "A reset link send to your email. Please check your email."
        )
        return super().form_valid(form)


class ForgotPasswordConfirmView(PasswordResetConfirmView):
    form_class = ForgotPasswordConfirmForm
    template_name = "reset-password.html"
    success_url = reverse_lazy("accounts:login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("core:home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(
            self.request, "Password reset successfully, you can login now."
        )
        return super().form_valid(form)


class UserProfileView(LoginRequiredMixin, TemplateView):
    login_url = "accounts:login"
    template_name = "profile/overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "profile"
        return context


class EditUserProfileView(LoginRequiredMixin, UpdateView):
    model = User
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
        response = super().form_valid(form)
        messages.success(self.request, "Your profile has been updated successfully!")
        return response

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


class GroupListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Group
    template_name = "admin/view/group-list.html"
    context_object_name = "groups"

    def test_func(self):
        return is_admin(self.request.user)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return redirect("core:no-permission")

    def get_queryset(self):
        return Group.objects.prefetch_related("permissions").all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Group List"
        return context


class CreateGroupView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Group
    form_class = CreateGroupForm
    template_name = "admin/form/create-group.html"
    success_url = reverse_lazy("accounts:group-list")

    def test_func(self):
        return is_admin(self.request.user)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return redirect("core:no-permission")

    def form_valid(self, form):
        group_name = form.instance.name
        response = super().form_valid(form)
        messages.success(
            self.request, f"Group '{group_name}' has been created successfully!"
        )
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong, please try again.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Group"
        return context


class UpdateGroupView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Group
    form_class = CreateGroupForm
    pk_url_kwarg = "id"
    template_name = "admin/form/create-group.html"
    login_url = "accounts:login"

    def test_func(self):
        return is_admin(self.request.user)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return redirect("core:no-permission")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Group updated successfully")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

    def get_success_url(self):
        obj = self.get_object()
        return reverse("accounts:update-group", args=[obj.pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Group"
        return context


class DeleteGroupView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Group
    pk_url_kwarg = "id"

    PROTECTED_GROUPS = {"Admin", "Organizer", "Participant"}

    def test_func(self):
        return is_admin(self.request.user)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return redirect("core:no-permission")

    def get(self, request, *args, **kwargs):
        messages.error(request, "Invalid request.")
        return redirect("accounts:group-list")

    def post(self, request, *args, **kwargs):
        group = cast(Group, self.get_object())

        if group.name in self.PROTECTED_GROUPS:
            messages.error(
                request,
                "You cannot delete a default group. Default groups are: Admin, Organizer, Participant.",
            )
            return redirect("accounts:group-list")

        try:
            group.delete()
            messages.success(request, "Group deleted successfully.")
        except Exception:
            messages.error(
                request,
                "Something went wrong while deleting the group. Please try again.",
            )
        return redirect("accounts:group-list")


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "admin/view/user-list.html"
    context_object_name = "users"

    def test_func(self):
        return is_admin(self.request.user)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return redirect("core:no-permission")

    def get_queryset(self):
        return User.objects.prefetch_related("groups").order_by("-date_joined")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "All Users"
        context["assign_form"] = AssignRoleForm()
        return context


class AssignRoleView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = AssignRoleForm
    success_url = reverse_lazy("accounts:user-list")
    pk_url_kwarg = "user_id"

    object: CustomUser

    def dispatch(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")

        if request.user.pk == user_id:
            messages.error(request, "You cannot assign a role to yourself.")
            return redirect("accounts:user-list")

        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        user_id = self.kwargs.get("user_id")
        return get_object_or_404(User, id=user_id)

    def form_valid(self, form):
        role = form.cleaned_data["role"]

        self.object.groups.clear()
        self.object.groups.add(role)

        messages.success(
            self.request,
            f"User '{self.object.username}' has been assigned to the '{role.name}' role.",
        )

        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong. Please try again.")
        return self.form_invalid(form)

    def test_func(self):
        return is_admin(self.request.user)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return redirect("core:no-permission")


class DeleteUserView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    success_url = reverse_lazy("accounts:user-list")
    pk_url_kwarg = "user_id"

    object: CustomUser

    def test_func(self):
        return is_admin(self.request.user)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return redirect("core:no-permission")

    def dispatch(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")

        if request.user.pk == user_id:
            messages.error(request, "You cannot delete yourself.")
            return redirect("accounts:user-list")

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = cast(CustomUser, self.get_object())
        username = user.username

        try:
            user.delete()
            messages.success(
                request, f"User '{username}' has been deleted successfully."
            )
        except Exception:
            messages.error(
                request,
                "Something went wrong while deleting the user. Please try again.",
            )

        return redirect("accounts:user-list")

    def get(self, request, *args, **kwargs):
        messages.error(request, "Invalid request.")
        return redirect("accounts:user-list")
