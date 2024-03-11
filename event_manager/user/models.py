from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Eigene Implementierung des User-Models.
    User-Model muss in den Settings hinterlegt sein.

    AUTH_USER_MODEL = "user.User"

    """

    # Beispiel: Address-Spalte einfügen
    address = models.CharField(max_length=200, blank=True, null=True)
