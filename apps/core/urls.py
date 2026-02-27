from django.urls import path

from .views import health_check, home_view, no_permission

app_name = "core"
urlpatterns = [
    path("", home_view, name="home"),
    path("no-permission/", no_permission, name="no-permission"),
    path("health/", health_check),
]
