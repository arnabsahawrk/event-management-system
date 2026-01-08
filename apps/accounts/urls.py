from django.urls import path

from .views import (
    activate_user,
    assign_role,
    create_group,
    delete_group,
    delete_user,
    group_list,
    login,
    logout,
    register,
    update_group,
    user_list,
    profile_page,
)

app_name = "accounts"
urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("profile/overview/", profile_page, name="overview"),
    path("admin/group-list/", group_list, name="group-list"),
    path("admin/create-group/", create_group, name="create-group"),
    path("admin/update-group/<int:id>/", update_group, name="update-group"),
    path("admin/delete-group/<int:id>/", delete_group, name="delete-group"),
    path("admin/user-list/", user_list, name="user-list"),
    path("admin/user-list/assign-role/<int:user_id>/", assign_role, name="assign-role"),
    path("admin/user-list/delete-user/<int:user_id>/", delete_user, name="delete-user"),
    path("activate/<int:user_id>/<str:token>/", activate_user),
]
