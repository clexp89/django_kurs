import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandParser
from events.models import Event, Category
from events.factories import CategoryFactory, EventFactory
from user.factories import UserFactory

User = get_user_model()

NUMBER_CATEGORIES = 10


class Command(BaseCommand):
    """Unser Kommando zum Generieren von Test-Events."""

    def add_arguments(self, parser: CommandParser) -> None:
        # python manage.py create_events -e 100, --events

        parser.description = "Generiere Events und Kategorien"
        parser.add_argument(
            "-e",
            "--events",
            type=int,
            required=True,
        )
        parser.epilog = "Nutzungsbeispiel: manage.py create_events --events=20"

    def handle(self, *args, **kwargs):
        number_events = kwargs.get("events")

        print("Deleting objects ...")
        for m in Event, Category:
            m.objects.all().delete()

        User.objects.exclude(username="admin").delete()
        userlist = UserFactory.create_batch(5)

        categories = CategoryFactory.create_batch(NUMBER_CATEGORIES)
        for _ in range(number_events):
            EventFactory(
                category=random.choice(categories),
                author=random.choice(userlist),
            )

        print("finished!")
