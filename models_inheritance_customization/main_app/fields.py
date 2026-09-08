from django.core.exceptions import ValidationError
from django.db import models


class StudentIDField(models.PositiveIntegerField):

    def get_db_prep_value(self, value, connection, prepared=False):
        try:
            value = int(value)
        except:
            raise ValueError("Invalid input for student ID")

        if value <= 0:
            raise ValidationError("ID cannot be less than or equal to zero")

        return value

class MaskedCreditCardField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if not isinstance(value, str):
            raise ValidationError("The card number must be a string")

        if not value.isdigit():
            raise ValidationError("The card number must contain only digits")

        if len(value) != 16:
            raise ValidationError("The card number must be exactly 16 characters long")

        return f"****-****-****-{value[-4:]}"

