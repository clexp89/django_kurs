""" 
Tests für das Prüfen von GET-Anfragen (public)

Prüfen:
- Eventliste öffentlich erreichbar
- EventDetail öffentlich erreichbar
"""

from http import HTTPStatus
from django.test import Client, TestCase
from django.urls import reverse
from events.factories import EventFactory


class TestEventPublicURLs(TestCase):
    def setUp(self):
        """Wird vor jeder Test-Methode ausgeührt"""
        self.client = Client()
        self.event = EventFactory()

    def test_events_overview(self):
        """Prüfen, ob die Event-Overview public erreichbar ist."""
        url = reverse("events:events")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, text="Übersicht")
        self.assertContains(response, text=self.event.name)

    def test_event_detail(self):
        """Prüfen, ob die Event-Detailseite public erreichbar ist."""
        url = reverse("events:event", kwargs={"pk": self.event.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, text=self.event.name)
