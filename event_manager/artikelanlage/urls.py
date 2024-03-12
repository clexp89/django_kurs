from django.urls import path
from .views import (
    ArtikelCreateView,
    ArtikelListView,
    ArtikelUpdateView,
    ArtikelDetailView,
)

app_name = "artikelanlage"

urlpatterns = [
    path("", ArtikelListView.as_view(), name="artikel_list"),
    path("create", ArtikelCreateView.as_view(), name="artikel_create"),
    path("update/<int:pk>", ArtikelUpdateView.as_view(), name="artikel_update"),
    path("<int:pk>", ArtikelDetailView.as_view(), name="artikel"),
]
