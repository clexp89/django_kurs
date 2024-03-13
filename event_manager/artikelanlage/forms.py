from django import forms

from .models import Artikel


class ArtikelForm(forms.ModelForm):
    class Meta:
        model = Artikel
        fields = "__all__"
        exclude = ("anforderer", "ist_angelegt")

        widgets = {
            "anforderungsdatum": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                },
            ),
        }


class ArtikelUpdateForm(ArtikelForm):
    class Meta(ArtikelForm.Meta):
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["anforderer"].disabled = True
