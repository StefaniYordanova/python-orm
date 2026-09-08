from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class RatingValidator:
    DEFAULT_MESSAGE: str = "The rating must be between 0.0 and 10.0"

    def __init__(self, message=DEFAULT_MESSAGE):
        self.message = message

    def __call__(self, value):
        if value < 0.0 or value > 10.0:
            raise ValidationError(self.message)


@deconstructible
class ReleaseYearValidator:
    DEFAULT_MESSAGE: str = "The release year must be between 1990 and 2023"

    def __init__(self, message=DEFAULT_MESSAGE):
        self.message = message

    def __call__(self, value):
        if value < 1990 or value > 2023:
            raise ValidationError(self.message)

