from django.urls import path
from . import views

app_name = "events"  # events:categories

urlpatterns = [
    path("", views.EventListView.as_view(), name="events"),
    path("create", views.EventCreateView.as_view(), name="event_create"),
    path("<int:pk>", views.EventDetailView.as_view(), name="event"),
    path("update/<int:pk>", views.EventUpdateView.as_view(), name="event_update"),
    # events/categories
    path("categories", views.categories, name="categories"),
    # events/categories/3
    path("categories/<int:pk>", views.category, name="category"),
    path(
        "category/create",
        views.category_create,
        name="category_create",
    ),
    path(
        "category/update/<int:pk>",
        views.category_update,
        name="category_update",
    ),
]
