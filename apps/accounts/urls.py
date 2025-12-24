from django.urls import path

from .views import group_list, login, logout, register

app_name = "accounts"
urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("admin/group-list", group_list, name="group-list"),
]
