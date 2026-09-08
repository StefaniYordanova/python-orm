from django.core.validators import MinValueValidator
from django.db import models
from .mixins import NameMixin, TimeStampUpdateMixin, TimeStampLaunchDateMixin
from .validators import OnlyDigitsValidator
from .querysets import AstronautCustomQuerySet

# Create your models here.

class Astronaut(NameMixin, TimeStampUpdateMixin):
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[
            OnlyDigitsValidator(),
        ]
    )
    is_active = models.BooleanField(
        default=True,
    )
    date_of_birth = models.DateField(
        null=True, blank=True,
    )
    spacewalks = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
        ]
    )

    objects = AstronautCustomQuerySet.as_manager()


class Spacecraft(NameMixin, TimeStampLaunchDateMixin, TimeStampUpdateMixin):
    manufacturer = models.CharField(
        max_length=100,
    )
    capacity = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
        ]
    )
    weight = models.FloatField(
        validators=[
            MinValueValidator(0.0),
        ]
    )


class Mission(NameMixin, TimeStampLaunchDateMixin, TimeStampUpdateMixin):

    class Status(models.TextChoices):
        PLANNED = 'Planned', 'Planned'
        ONGOING = 'Ongoing', 'Ongoing'
        COMPLETED = 'Completed', 'Completed'

    description = models.TextField(
        null=True, blank=True,
    )
    status = models.CharField(
        max_length=9,
        default='Planned',
        choices=Status.choices,
    )
    spacecraft = models.ForeignKey(
        to='Spacecraft',
        on_delete=models.CASCADE,
        related_name='missions',
    )
    astronauts = models.ManyToManyField(
        to='Astronaut',
        related_name='missions',
    )
    commander = models.ForeignKey(
        to='Astronaut',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='commanded_missions',
    )
