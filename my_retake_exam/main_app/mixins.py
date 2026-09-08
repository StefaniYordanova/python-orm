from django.core.validators import MinLengthValidator
from django.db import models


class NameMixin(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(
        max_length=80,
        validators=[
            MinLengthValidator(5),
        ],
        unique=True,
    )


class WinsMixin(models.Model):
    class Meta:
        abstract = True

    wins = models.PositiveSmallIntegerField(
        default=0,
    )


class TimeStampModification(models.Model):
    class Meta:
        abstract = True

    modified_at = models.DateTimeField(
        auto_now=True,
    )
