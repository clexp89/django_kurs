from django import forms
from django.core.exceptions import ValidationError
from . import models


class FileUploadForm(forms.Form):
    files = forms.FileField(
        widget=forms.TextInput(
            attrs={
                "type": "File",
                "multiple": True,
                "accept": "text/plain,application/msword",
            }
        ),
        label="File Upload",
    )


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
        exclude = ("author", "category")

        widgets = {
            "date": forms.DateInput(
                format="%Y-%m-%d %H:%M",
                attrs={
                    "type": "datetime-local",
                },
            ),
        }

    # message = forms.CharField(max_length=30)

    def clean_message(self) -> str:
        message = self.cleaned_data["message"]
        print("My message:", message)
        return message

    def clean_sub_title(self) -> str:
        """
        Clean-Methoden haben die Form: clean_<FELDNAME>
        """

        sub_title = self.cleaned_data["sub_title"]

        if isinstance(sub_title, str) and sub_title.startswith(("*", "#", "-")):
            raise ValidationError("Subtitle ist nicht valid")

        return sub_title

    def clean(self):
        super().clean()  # führt die clean-Methoden aus

        category = self.cleaned_data.get("category")
        sub_title_value = self.cleaned_data.get("sub_title")

        if category and sub_title_value:
            if category.name == "Science" and "science" in sub_title_value:
                self._errors["sub_title"] = self.error_class(
                    ["Kategorie Science verbietet science in Subtitle"]
                )
                raise ValidationError("Kategorie Science verbietet science in Subtitle")
