import factory
from typing import Final
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

PASSWORD: Final = "abc"


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.LazyFunction(
        lambda: make_password(PASSWORD),
    )
