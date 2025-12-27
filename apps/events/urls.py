from django.urls import path

from apps.events.views import (
    create_form,
    delete,
    dashboard,
    rsvp_delete,
    rsvp_events,
    rsvp_view,
    seed_demo_data,
    update_form,
    view_all,
)

app_name = "events"
urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("view-all/", view_all, name="view-all"),
    path("create-form/", create_form, name="create-form"),
    path("update-form/<int:id>/", update_form, name="update-form"),
    path("delete/<int:id>/", delete, name="delete"),
    path("dashboard/rsvp/<int:event_id>/", rsvp_events, name="rsvp"),
    path("rsvp-view/", rsvp_view, name="rsvp-view"),
    path("rsvp-delete/<int:id>/", rsvp_delete, name="rsvp-delete"),
    path("seed-demo/", seed_demo_data),
]
