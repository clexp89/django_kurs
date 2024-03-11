from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class DateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # beim Anlegen
    updated_at = models.DateTimeField(auto_now=True)  # beim Updaten aktualisieren

    class Meta:
        abstract = True  # lege keine Tabelle dafür an


class Category(DateMixin):
    """Kategorie eines Events."""

    name = models.CharField(
        max_length=100,
        unique=True,
    )
    sub_title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(help_text="Beschreibung der Kategorie")

    class Meta:
        verbose_name = "Kategorie"
        verbose_name_plural = "Kategorien"
        ordering = ["name"]  # Default-Sortierung

    def __str__(self) -> str:
        return self.name


class Event(DateMixin):
    """Event Model."""

    class Group(models.IntegerChoices):
        SMALL = 2, "kleine Gruppe"
        MEDIUM = 5, "mittelgroße Gruppe"
        BIG = 10, "große Gruppe"
        UNLIMITED = 0, "keine Begrenzung"

    name = models.CharField(
        max_length=200,
    )
    sub_title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(
        help_text="Beschreibung des Events", verbose_name="Beschreibung"
    )
    date = models.DateTimeField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="events",
        verbose_name="Kategorie",
    )
    is_active = models.BooleanField(default=True)
    min_group = models.PositiveSmallIntegerField(choices=Group.choices)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")

    def related_events(self):
        """Alle Events, die diesem Event ähnlich sind."""
        related_events = Event.objects.filter(
            min_group=self.min_group, category=self.category
        )
        return related_events.exclude(pk=self.pk)

    def __str__(self) -> str:
        return self.name