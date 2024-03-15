from rest_framework.serializers import ModelSerializer
from events.models import Event, Category


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        # exclude = ("author",)
        extra_kwargs = {
            "author": {
                "read_only": True,
            },
        }
