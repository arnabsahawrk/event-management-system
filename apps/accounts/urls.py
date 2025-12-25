from django.urls import path

from .views import (
    create_group,
    delete_group,
    group_list,
    login,
    logout,
    register,
    update_group,
)

app_name = "accounts"
urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("admin/group-list", group_list, name="group-list"),
    path("admin/create-group", create_group, name="create-group"),
    path("admin/update-group/<int:id>/", update_group, name="update-group"),
    path("admin/delete-group/<int:id>/", delete_group, name="delete-group"),
]
