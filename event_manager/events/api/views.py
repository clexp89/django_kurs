from rest_framework import generics, authentication, permissions
from events.models import Event, Category
from .serializers import EventSerializer
from .permissions import IsOwnerOrReadonly


class EventListCreateAPIView(generics.ListCreateAPIView):
    """View zum Auflisten und Anlegen von neuen Event-Objekten."""

    queryset = Event.objects.all()
    serializer_class = EventSerializer

    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def perform_create(self, serializer) -> None:
        """Zum Einfügen von Daten vor dem Speichern in der DB."""
        author = self.request.user
        serializer.save(author=author)


class EventDetailUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """View zum Auflisten eines Objekts und zum Updaten und Löschen."""

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    ]
    permission_classes = [
        IsOwnerOrReadonly,
    ]
