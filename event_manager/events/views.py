from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.http import HttpResponse
from . import models
from .forms import CategoryForm, EventForm


class EventCreateView(CreateView):
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

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EventUpdateView(UpdateView):
    """
    events/3/update/
    Default-Template: event_form.html
    falls get_absolute_url implementiert ist, wird dorthin
    weitergeleitet
    """

    model = models.Event
    form_class = EventForm


class EventDetailView(DetailView):
    """
    events/3
    Default-Template: event_detail.html
    """

    model = models.Event


class EventListView(ListView):
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
