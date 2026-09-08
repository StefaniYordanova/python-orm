from collections.abc import Callable

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

# Option 1: -> with class
@deconstructible
class OnlyDigitsValidator:

    def __init__(self, message: str = None):
        self.message = message

    def __call__(self, value: str):
        if not value.isdigit():
            raise ValidationError(self.message)


# Option 2: -> with functions
# 2.1.
def contains_only_digits_validator(value: str) -> None:
    if not value.isdigit():
        raise ValidationError()

# 2.2.
def contains_only_digits_validator_with_message(message: Optional[str] = None) -> Callable:
    def validator(value: str) -> None:
        if not value.isdigit():
            raise ValidationError(message)

    return validator
