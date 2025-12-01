from django.urls import path

from events.views import organizer_dashboard, view_all

urlpatterns = [
    path("organizer-dashboard/", organizer_dashboard, name="organizer-dashboard"),
    path("view-all/", view_all, name="view-all"),
]
