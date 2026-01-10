from django.urls import path

from .views import (
    RegisterView,
    CustomLoginView,
    CustomLogoutView,
    ActiveUserView,
    UserProfileView,
    EditUserProfileView,
    ChangeUserPasswordView,
    GroupListView,
    CreateGroupView,
    UpdateGroupView,
    DeleteGroupView,
    UserListView,
    AssignRoleView,
    DeleteUserView,
)

app_name = "accounts"
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("activate/<int:user_id>/<str:token>/", ActiveUserView.as_view()),
    path("profile/overview/", UserProfileView.as_view(), name="overview"),
    path("profile/edit/", EditUserProfileView.as_view(), name="edit"),
    path("profile/password/", ChangeUserPasswordView.as_view(), name="password"),
    path("admin/group-list/", GroupListView.as_view(), name="group-list"),
    path("admin/create-group/", CreateGroupView.as_view(), name="create-group"),
    path(
        "admin/update-group/<int:id>/", UpdateGroupView.as_view(), name="update-group"
    ),
    path(
        "admin/delete-group/<int:id>/", DeleteGroupView.as_view(), name="delete-group"
    ),
    path("admin/user-list/", UserListView.as_view(), name="user-list"),
    path(
        "admin/user-list/assign-role/<int:user_id>/",
        AssignRoleView.as_view(),
        name="assign-role",
    ),
    path(
        "admin/user-list/delete-user/<int:user_id>/",
        DeleteUserView.as_view(),
        name="delete-user",
    ),
]
