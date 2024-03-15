from django.urls import path
from . import views

urlpatterns = [
    # api/events
    path(
        "events",
        views.EventListCreateAPIView.as_view(),
        name="list_create_events",
    ),
    path(
        "events/<int:pk>",
        views.EventDetailUpdateAPIView.as_view(),
        name="retrieve_update_events",
    ),
]
