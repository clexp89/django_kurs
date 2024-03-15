import json
import pathlib
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.exceptions import BadRequest
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.conf import settings

from .models import Artikel
from .forms import ArtikelForm, ArtikelUpdateForm
from .serializers import ArtikelSerializer


class VerhindereEditMixin:
    def get_initial(self) -> dict:
        if self.object.ist_angelegt:
            raise BadRequest("Diese Aktion ist nicht erlaubt")
        return super().get_initial()


class ArtikelDetailView(DetailView):
    model = Artikel


class ArtikelListView(ListView):
    model = Artikel
    # queryset = Artikel.objects.filter(ist_angelegt=False)

    def get_queryset(self) -> QuerySet:
        qs = Artikel.objects.all()

        angelegt = self.request.GET.get("angelegt")
        if angelegt and angelegt == "1":
            qs = qs.filter(ist_angelegt=True)
        elif angelegt and angelegt == "2":
            qs = qs.filter(ist_angelegt=False)

        return qs


class ArtikelUpdateView(
    VerhindereEditMixin,
    SuccessMessageMixin,
    LoginRequiredMixin,
    UpdateView,
):
    """
    artikelanlage/update/3
    """

    model = Artikel
    form_class = ArtikelUpdateForm
    success_message = "Artikel wurde erfolgreich editiert"


def save_model_to_json(model):
    try:
        s = ArtikelSerializer(model)

        with open(settings.JSON_DATA_DIR / "data.json", mode="w") as f:
            json.dump(s.data, f, indent=4)
            return True
    except:
        # todo: LOG ERROR
        pass
    return False


class ArtikelCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """
    artikelanlage/create
    """

    model = Artikel
    form_class = ArtikelForm
    success_url = reverse_lazy("artikelanlage:artikel_list")
    success_message = "Artikel wurde erfolgreich angelegt"

    def form_valid(self, form):
        form.instance.anforderer = self.request.user
        result = save_model_to_json(form.instance)
        if result:
            messages.info(
                self.request, "Json wurde erfolgreich serialisiert und gespeichert."
            )

        return super().form_valid(form)


class ArtikelDeleteView(
    VerhindereEditMixin,
    SuccessMessageMixin,
    LoginRequiredMixin,
    DeleteView,
):
    """
    artikelanlage/delete/3

    artikel_delete_confirm.html
    """

    model = Artikel
    success_url = reverse_lazy("artikelanlage:artikel_list")
    success_message = "Artikel wurde erfolgreich gelöscht"

    def get_initial(self) -> dict:
        if self.object.ist_angelegt:
            raise BadRequest("Diese Aktion ist nicht erlaubt")
        return super().get_initial()
