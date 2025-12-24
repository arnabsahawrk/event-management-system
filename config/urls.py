from django.contrib import admin
from django.urls import include, path
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("events/", include("apps.events.urls")),
    path("accounts/", include("apps.accounts.urls")),
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
