from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from event_manager.mixins import DateMixin

User = get_user_model()


class Konto(DateMixin):
    nummer = models.PositiveIntegerField(unique=True)
    bezeichnung = models.CharField(max_length=40)

    def __str__(self) -> str:
        return f"{self.bezeichnung} ({self.nummer})"


class Lieferant(DateMixin):

    class Gruppe(models.TextChoices):
        ELEKTRO = "elektro"
        STAHL = "stahl"
        HYDRAULIK = "hydraulik"

    nummer = models.PositiveIntegerField(unique=True)
    bezeichnung_1 = models.CharField(max_length=40)
    bezeichnung_2 = models.CharField(max_length=40, null=True, blank=True)
    gruppe = models.CharField(max_length=20, choices=Gruppe.choices)

    class Meta:
        verbose_name = "Lieferant"
        verbose_name_plural = "Lieferanten"

    def __str__(self) -> str:
        return f"{self.bezeichnung_1} ({self.nummer})"


class Artikel(DateMixin):
    class Einheit(models.TextChoices):
        KG = "KG"
        METER = "M"
        STUECK = "stk."

    nummer = models.CharField(max_length=8, null=True, blank=True)
    mengeneinheit = models.CharField(max_length=8, choices=Einheit.choices)
    bezeichnung_1 = models.CharField(max_length=40)
    bezeichnung_2 = models.CharField(max_length=40, null=True, blank=True)
    lieferant = models.ForeignKey(
        Lieferant, on_delete=models.SET_NULL, null=True, blank=True
    )
    lieferant_artikel_nr = models.CharField(max_length=40, null=True, blank=True)
    konto = models.ForeignKey(Konto, on_delete=models.PROTECT)
    zeichnungs_nummer = models.CharField(max_length=20, null=True, blank=True)
    anforderer = models.ForeignKey(User, on_delete=models.PROTECT)
    gewicht = models.DecimalField(
        max_digits=10, decimal_places=3, null=True, blank=True
    )
    ist_angelegt = models.BooleanField(default=False)
    anforderungsdatum = models.DateField()

    class Meta:
        verbose_name = "Artikel"
        verbose_name_plural = "Artikel"

    def __str__(self) -> str:
        return f"{self.bezeichnung_1} ({self.nummer})"

    def get_absolute_url(self):
        return reverse("artikelanlage:artikel", kwargs={"pk": self.pk})
