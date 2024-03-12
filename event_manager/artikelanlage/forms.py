from django import forms

from .models import Artikel


class ArtikelForm(forms.ModelForm):
    class Meta:
        model = Artikel
        fields = "__all__"

        widgets = {
            "anforderungsdatum": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                },
            ),
        }
