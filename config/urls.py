from django.contrib import admin
from django.urls import include, path
from django.conf import settings

from theme.views import home_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),
    path("events/", include("events.urls")),
]

if settings.DEBUG:
    try:
        from debug_toolbar.toolbar import debug_toolbar_urls

        urlpatterns += debug_toolbar_urls()
        urlpatterns += [
            path("__reload__/", include("django_browser_reload.urls")),
        ]
    except ImportError:
        pass
