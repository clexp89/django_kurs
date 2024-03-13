from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.contrib import messages
from . import models
from .forms import CategoryForm, EventForm


def is_moderator(user):
    return user.groups.filter(name="Moderatoren").exists()


class UserIsOwnerMixin(UserPassesTestMixin):
    def test_func(self) -> bool | None:
        return (self.request.user == self.get_object().author) or is_moderator(
            self.request.user
        )


class EventCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    events/create
    Default-Template: event_form.html
    falls get_absolute_url implementiert ist, wird dorthin
    weitergeleitet

    Todo: Prüfen, ob eingeloggt
    """

    model = models.Event
    form_class = EventForm
    # success_url = "events:events"
    success_message = "Event wurde erfolgreich eingetragen"

    def form_valid(self, form):
        print("form:", form.__dict__)
        print(self.request.POST)
        form.instance.author = self.request.user
        return super().form_valid(form)


class EventDeleteView(UserIsOwnerMixin, SuccessMessageMixin, DeleteView):
    """
    events/3/delete
    Default-Template: event_confirm_delete.html
    hier muss success_url implementiert werden!
    """

    model = models.Event
    success_message = "Event wurde erfolgreich gelöscht"
    success_url = reverse_lazy("events:events")


class EventUpdateView(UserIsOwnerMixin, SuccessMessageMixin, UpdateView):
    """
    events/3/update/
    Default-Template: event_form.html
    falls get_absolute_url implementiert ist, wird dorthin
    weitergeleitet
    """

    model = models.Event
    form_class = EventForm
    success_message = "Event wurde erfolgreich eingetragen"


class EventDetailView(DetailView):
    """
    events/3
    Default-Template: event_detail.html
    """

    model = models.Event


class EventListView(LoginRequiredMixin, ListView):
    """
    events/
    Default-Template: event_list.html
    """

    model = models.Event
    queryset = models.Event.objects.select_related("category", "author")
    # template_name


def category_update(request, pk) -> HttpResponse:
    """
    events/catetory/update/3 GET und POST auf
    """
    category = get_object_or_404(models.Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        messages.warning(request, "hier wurde etwas eingetragen.")
        messages.info(request, "eine Info meldung")
        category = form.save()
        return redirect(category)

    return render(
        request,
        "events/category_create.html",
        {
            "form": form,
            "category": category,
        },
    )


def category_create(request) -> HttpResponse:
    """
    events/category/create GET und POST auf
    """
    if request.method == "POST":
        form = CategoryForm(request.POST or None)
        if form.is_valid():
            category = form.save(commit=True)  # commit=False speichert nicht in DB
            # category.author = request.user
            # category.save()
            # return redirect("events:categories")  # Redirect auf Übersichtsseite
            return redirect(category)
    else:
        form = CategoryForm()

    return render(
        request,
        "events/category_create.html",
        {"form": form},
    )


def category(request, pk) -> HttpResponse:
    """
    events/categories/3
    """
    # category = models.Category.objects.get(pk=pk)
    category = get_object_or_404(models.Category, pk=pk)
    return render(
        request,
        "events/category.html",
        {"category": category},
    )


def categories(request) -> HttpResponse:
    """
    events/categories
    """
    categories = models.Category.objects.all()
    # categories = models.Category.objects.none()  # leeres QS
    # return HttpResponse(categories)
    return render(
        request,
        "events/categories.html",
        {"categories": categories},
    )
