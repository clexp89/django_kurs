from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.deconstruct import deconstructible


@deconstructible
class BadWordFilter:
    """Prüfe, ob in field_value ein Begriff aus word_list enthalten ist.
    wird als BadWordFilter(["evil", "bad"]) in validators gepackt.
    """

    def __init__(self, evil_word_list: list[str]):
        self.evil_word_list = evil_word_list

    def __call__(self, field_value: str):
        for word in field_value.split():
            if word in self.evil_word_list:
                raise ValidationError(f"Dieses Wort ist nicht erlaubt: {word}")


def bad_word_filter(evil_word_list: list[str], field_value: str) -> None:
    """Prüfe, ob in field_value ein Begriff aus word_list enthalten ist.
    muss dann mit partial(bad_word_filter["evil", "bad"]) in validators
    gepackt werden.
    """
    for word in field_value.split():
        if word in evil_word_list:
            raise ValidationError("Dieses Wort ist nicht erlaubt")


def datetime_in_future(field_value) -> None:
    """Prüfen, ob ein Datetime in der Vergangenheit liegt.

    Raises:
        ValidationError (falls True)
    """
    if field_value < timezone.now():
        raise ValidationError("Der Zeitpunkt darf nicht in der Vergangenheit liegen!")
