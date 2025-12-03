from django.urls import path

from events.views import (
    create_form,
    delete,
    organizer_dashboard,
    update_form,
    view_all,
)

urlpatterns = [
    path("organizer-dashboard/", organizer_dashboard, name="organizer-dashboard"),
    path("view-all/", view_all, name="view-all"),
    path("create-form/", create_form, name="create-form"),
    path("update-form/<int:id>/", update_form, name="update-form"),
    path("delete/<int:id>/", delete, name="delete"),
]
