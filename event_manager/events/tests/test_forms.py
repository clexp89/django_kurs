""" 
Tests für das Prüfen von Formular-Anfragen (POST)

Prüfen:
- Event eintragen möglich für eingeloggten User
- Event eintragen nicht möglich für nicht eingeloggten User
"""

import logging
from datetime import datetime, timedelta
from django.utils import timezone
from pprint import pprint
from http import HTTPStatus
from django.test import Client, TestCase
from django.urls import reverse
from django.forms.models import model_to_dict
from events.factories import EventFactory, CategoryFactory
from user.factories import UserFactory
from events.models import Event

logging.disable(logging.DEBUG)


class CategoryFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.payload = {
            "name": "TestCate",
            "description": "asdfsadfd",
        }

    def test_create_categroy_valid_data(self):
        url = reverse("events:category_create")
        response = self.client.post(url, self.payload)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


class EventFormTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()
        cls.category = CategoryFactory()

    def setUp(self):
        self.client = Client()
        self.payload = model_to_dict(
            EventFactory(), exclude=["id", "author", "category"]
        )
        self.create_url = reverse(
            "events:event_create", kwargs={"category_id": self.category.pk}
        )

    def test_proper_data(self):
        """Prüfen, ob Eintragen mit validen Daten möglich ist."""

        self.client.force_login(self.user)

        # GET
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "events/event_form.html")

        # POST
        response = self.client.post(self.create_url, self.payload)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Event.objects.count(), 2)
        # Prüfen, ob der Redirect auf die richtige Seite geht
        self.assertRedirects(
            response,
            expected_url=reverse("events:category", kwargs={"pk": self.category.pk}),
        )

    # Aufgabe: Test invalid Daten, zb. min group 3, nur POST
    def test_invalid_min_group(self):
        self.client.force_login(self.user)
        self.payload["min_group"] = 23
        response = self.client.post(self.create_url, self.payload)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Event.objects.count(), 1)
        self.assertTemplateUsed(response, "events/event_form.html")
