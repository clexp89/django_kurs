from rest_framework import serializers
from .models import Artikel, Konto


class KontoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Konto
        fields = "__all__"


class ArtikelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artikel
        exclude = ("gewicht", "id", "created_at", "updated_at")

    lieferant = serializers.StringRelatedField()
    konto = KontoSerializer(many=False, read_only=True)
    # konto = serializers.StringRelatedField()
    anforderer = serializers.StringRelatedField()
