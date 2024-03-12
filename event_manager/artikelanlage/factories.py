import random
import factory
from datetime import timedelta

from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Artikel
from faker import Factory as FakerFactory

faker = FakerFactory.create()


class ArtikelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Artikel

    nummer = factory.LazyAttribute(
        lambda e: str(random.randint(1000000, 9999999)),
    )
    mengeneinheit = factory.LazyAttribute(
        lambda e: random.choice(Artikel.Einheit.values)
    )
    bezeichnung_1 = factory.LazyAttribute(lambda n: faker.sentence()[:40])
    bezeichnung_2 = factory.LazyAttribute(lambda n: faker.sentence()[:40])
    anforderer = factory.Iterator(get_user_model().objects.all())
    ist_angelegt = factory.Faker("boolean", chance_of_getting_true=50)
    anforderungsdatum = factory.Faker("date")
