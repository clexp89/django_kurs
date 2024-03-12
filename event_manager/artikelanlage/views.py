from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Artikel
from .forms import ArtikelForm


class ArtikelDetailView(DetailView):
    model = Artikel


class ArtikelListView(ListView):
    model = Artikel


class ArtikelUpdateView(UpdateView):
    """
    artikelanlage/update/3
    """

    model = Artikel
    form_class = ArtikelForm


class ArtikelCreateView(CreateView):
    """
    artikelanlage/create
    """

    model = Artikel
    form_class = ArtikelForm
    success_url = reverse_lazy("artikelanlage:artikel_list")
