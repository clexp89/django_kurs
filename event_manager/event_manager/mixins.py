from django.db import models


class DateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # beim Anlegen
    updated_at = models.DateTimeField(auto_now=True)  # beim Updaten aktualisieren

    class Meta:
        abstract = True  # lege keine Tabelle dafür an
