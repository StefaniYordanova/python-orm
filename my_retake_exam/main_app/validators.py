from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class CodeValidator:
    def __init__(self, message: str = None):
        self.message = message

    def __call__(self, value: str):
        for l in value:
            if not l.isalpha() or l != '#':
                raise ValidationError(self.message)

