import logging
from pathlib import Path
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.contrib import messages
from . import models
from .forms import CategoryForm, EventForm, FileUploadForm
from django.conf import settings

logger = logging.getLogger("events")


def is_moderator(user):
    return user.groups.filter(name="Moderatoren").exists()


class UserIsOwnerMixin(UserPassesTestMixin):
    def test_func(self) -> bool | None:
        return (self.request.user == self.get_object().author) or is_moderator(
            self.request.user
        )


def handle_uploaded_files(files):
    # save_to = Path(__file__).parent.parent / "data"
    save_to = settings.JSON_DATA_DIR
    for f in files:
        filepath = save_to / f.name
        with open(filepath, "wb+") as dest:
            # write in chunks to avoid RAM overflow
            for chunk in f.chunks():
                dest.write(chunk)


def upload_files(request):
    """View zum Hochladen und Verarbeiten von Dateien."""
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        files = request.FILES.getlist("files")
        handle_uploaded_files(files)
        # return redirect()
        return HttpResponse("Files successfully uploaded")
    else:
        form = FileUploadForm()

    return render(request, "events/file_upload.html", {"form": form})


class EventCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    für Kategorie 3 einen Event anlegen
    events/create/3
    Default-Template: event_form.html
    falls get_absolute_url implementiert ist, wird dorthin
    weitergeleitet

    """

    model = models.Event
    form_class = EventForm
    success_message = "Event wurde erfolgreich eingetragen"

    def get_initial(self) -> dict:
        """Prüfen, ob die gewählte Kategorie überhaupt existiert."""
        self.category = get_object_or_404(
            models.Category, pk=self.kwargs["category_id"]
        )
        # Über initial
        initial = super().get_initial()
        # initial["category"] = self.kwargs["category_id"]
        return initial

    def form_valid(self, form):

        # Kategorie und Author mit Werten belegen
        form.instance.category = self.category
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return self.category.get_absolute_url()


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


class EventListView(ListView):
    """
    events/
    Default-Template: event_list.html
    """

    model = models.Event
    # queryset = models.Event.active_objects.select_related("category", "author")
    queryset = models.Event.objects.active().travel()
    paginate_by = 5

    def get_context_data(self, **kwargs) -> dict:
        ctx = super().get_context_data(**kwargs)
        ctx["suchwort"] = self.s
        return ctx

    def get_queryset(self):

        qs = super().get_queryset()
        search_str = self.request.GET.get("q")
        self.s = search_str
        logger.info(f"Suchwort war {search_str}")
        if search_str:
            # /events/?q=test
            new_qs = qs.filter(
                Q(name__contains=search_str) | Q(sub_title__contains=search_str)
            )
            if not new_qs:
                messages.warning(self.request, "Begriff wurde nicht gefunden.")
                return new_qs
            else:
                qs = new_qs

        return qs


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
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)  # commit=False speichert nicht in DB
            form.save()
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
