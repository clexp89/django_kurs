import random
from django.core.management.base import BaseCommand, CommandParser
from artikelanlage.models import Konto, Lieferant
from artikelanlage.factories import ArtikelFactory

NUMBER_ARTIKEL = 10


class Command(BaseCommand):
    """Unser Kommando zum Generieren von Test-Artikeln."""

    def handle(self, *args, **kwargs):
        kontos = Konto.objects.all()
        lieferanten = Lieferant.objects.all()

        for _ in range(NUMBER_ARTIKEL):
            ArtikelFactory(
                konto=random.choice(kontos),
                lieferant=random.choice(lieferanten),
            )
