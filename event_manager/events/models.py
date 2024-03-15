from functools import partial
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from event_manager.mixins import DateMixin
from . import validators
from .managers import ActiveManager, SuperManager, EventQuerySet

User = get_user_model()


class Category(DateMixin):
    """Kategorie eines Events."""

    name = models.CharField(
        max_length=100,
        unique=True,
    )
    sub_title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(help_text="Beschreibung der Kategorie")
    image = models.FileField(upload_to="images", null=True, blank=True)

    class Meta:
        verbose_name = "Kategorie"
        verbose_name_plural = "Kategorien"
        ordering = ["name"]  # Default-Sortierung

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        # Verlinkung auf Detailseite der Kategorie
        return reverse("events:category", kwargs={"pk": self.pk})

    def get_events(self):
        return Event.objects.select_related("author").filter(category=self)


class Event(DateMixin):
    """Event Model."""

    class Group(models.IntegerChoices):
        SMALL = 2, "kleine Gruppe"
        MEDIUM = 5, "mittelgroße Gruppe"
        BIG = 10, "große Gruppe"
        UNLIMITED = 0, "keine Begrenzung"

    name = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(3, message="Name ist kurz!"),
        ],
    )
    sub_title = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="Wenn Kategorie science, darf hier nicht science stehen",
    )
    description = models.TextField(
        help_text="Beschreibung des Events",
        verbose_name="Beschreibung",
        validators=[
            validators.BadWordFilter(evil_word_list=["evil", "doof"])
            # partial(validators.bad_word_filter, ["evil", "doof"]),
        ],
    )
    date = models.DateTimeField(
        validators=[
            validators.datetime_in_future,
        ]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="events",
        verbose_name="Kategorie",
    )
    is_active = models.BooleanField(default=True)
    min_group = models.PositiveSmallIntegerField(choices=Group.choices)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")

    # der objects-Manager (default) muss oben stehen.
    objects = SuperManager.from_queryset(EventQuerySet)()
    # Event.objects.active().all()
    # active_objects = ActiveManager()

    class Meta:
        ordering = ["name"]

    def related_events(self):
        """Alle Events, die diesem Event ähnlich sind."""
        related_events = Event.objects.filter(
            min_group=self.min_group, category=self.category
        )
        return related_events.exclude(pk=self.pk)

    def get_absolute_url(self):
        return reverse("events:event", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.name

    # def clean(self) -> None:
    #     """Crossfield Validation auf Model-Ebene."""
    #     if self.category.name == "Science" and not self.is_active:
    #         raise ValidationError(
    #             "Wenn Sciene ausgewählt ist, muss das Event aktiv sein"
    #         )
