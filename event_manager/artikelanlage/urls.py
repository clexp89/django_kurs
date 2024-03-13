from django.urls import path
from .views import (
    ArtikelCreateView,
    ArtikelListView,
    ArtikelUpdateView,
    ArtikelDetailView,
    ArtikelDeleteView,
)

app_name = "artikelanlage"

urlpatterns = [
    path("", ArtikelListView.as_view(), name="artikel_list"),
    path("create", ArtikelCreateView.as_view(), name="artikel_create"),
    path("update/<int:pk>", ArtikelUpdateView.as_view(), name="artikel_update"),
    path("delete/<int:pk>", ArtikelDeleteView.as_view(), name="artikel_delete"),
    path("<int:pk>", ArtikelDetailView.as_view(), name="artikel"),
]
