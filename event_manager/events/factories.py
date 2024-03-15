import random
import factory
from datetime import timedelta

from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Category, Event
from user.factories import UserFactory

categories = [
    "Sports",
    "Talk",
    "Cooking",
    "Freetime",
    "Hiking",
    "Movies",
    "Travelling",
    "Science",
    "Arts",
    "Pets",
    "Music",
    "Wellness",
]


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Iterator(categories)
    sub_title = factory.Faker("sentence")
    description = factory.Faker("paragraph", nb_sentences=10)


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    author = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    name = factory.Faker("sentence")
    sub_title = factory.Faker("sentence")
    description = factory.Faker("paragraph", nb_sentences=10)
    date = factory.Faker(
        "date_time_between",
        start_date=timezone.now(),
        end_date=timezone.now() + timedelta(days=100),
        tzinfo=timezone.get_current_timezone(),
    )

    # author = factory.Iterator(get_user_model().objects.all())
    min_group = factory.LazyAttribute(lambda e: random.choice(Event.Group.values))
