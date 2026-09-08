from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models


class PersonalInfoMixin(models.Model):

    class Meta:
        abstract = True

    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3),
        ]
    )
    country = models.CharField(
        max_length=40,
        default='TBC',
    )


class RatingMixin(models.Model):

    class Meta:
        abstract = True

    rating = models.FloatField(
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0),
        ],
        default=0.0,
    )


class TimeStampUpdatedMixin(models.Model):

    class Meta:
        abstract = True

    updated_at = models.DateTimeField(auto_now=True)

