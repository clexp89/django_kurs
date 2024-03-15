from django.db import models


class EventQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def sport(self):
        """Filtere Sport-Objekte"""
        return self.filter(category__name="Sports")

    def talk(self):
        """Filtere Sport-Objekte"""
        return self.filter(category__name="Talk")

    def travel(self):
        """Filtere Sport-Objekte"""
        return self.filter(category__name="Travelling")


class SuperManager(models.Manager):
    """Supermanager basiert auf einem eigenen Queryset und
    ermöglicht das Chainen von Abfragen.
    Event.objects.active().travel()
    """

    def get_queryset(self) -> models.QuerySet:
        return EventQuerySet(self.model, using=self._db).select_related(
            "author", "category"
        )


class ActiveManager(models.Manager):
    """Einfacher Manager, der ein Queryset mit aktiven Objekten erstellt."""

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_active=True)
