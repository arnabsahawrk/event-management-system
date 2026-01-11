from django.urls import path

from apps.events.views import (
    DashboardView,
    CreateFormView,
    DeleteFormView,
    UpdateFormView,
    ViewAllView,
    RSVPView,
    RSVPEventView,
    RSVPDeleteView,
)

app_name = "events"
urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("view-all/", ViewAllView.as_view(), name="view-all"),
    path("create-form/", CreateFormView.as_view(), name="create-form"),
    path("update-form/<int:id>/", UpdateFormView.as_view(), name="update-form"),
    path("delete/<int:id>/", DeleteFormView.as_view(), name="delete"),
    path("rsvp-view/", RSVPView.as_view(), name="rsvp-view"),
    path("dashboard/rsvp/<int:event_id>/", RSVPEventView.as_view(), name="rsvp"),
    path("rsvp-delete/<int:id>/", RSVPDeleteView.as_view(), name="rsvp-delete"),
]
