from django.contrib import admin
from django.urls import include, path
from django.conf import settings

urlpatterns = [
    path("", include("apps.core.urls")),
    path("events/", include("apps.events.urls")),
    path("accounts/", include("apps.accounts.urls")),
]


if settings.DEBUG:
    urlpatterns += [
        path("admin/", admin.site.urls),
        path("__debug__/", include("debug_toolbar.urls")),
        path("__reload__/", include("django_browser_reload.urls")),
    ]
