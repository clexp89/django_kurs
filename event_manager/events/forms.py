from django import forms
from . import models


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = "__all__"  # alernativ ("name", "sub_title", ...)

        labels = {
            "name": "Name der Kategorie",
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = models.Event
        fields = "__all__"
        exclude = ("author",)

        widgets = {
            "date": forms.DateInput(
                format="%Y-%m-%d %H:%M",
                attrs={
                    "type": "datetime-local",
                },
            ),
        }
