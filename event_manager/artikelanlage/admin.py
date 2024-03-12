from django.contrib import admin
from . import models


@admin.register(models.Konto)
class KontoAdmin(admin.ModelAdmin):
    list_display = ("id", "nummer")


@admin.register(models.Lieferant)
class LieferantAdmin(admin.ModelAdmin):
    list_display = ("id", "nummer", "bezeichnung_1", "gruppe")


@admin.register(models.Artikel)
class ArtikelAdmin(admin.ModelAdmin):
    list_display = ("id", "nummer", "bezeichnung_1", "lieferant", "ist_angelegt")
