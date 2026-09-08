from datetime import date
from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.db import models
from .mixins import NameMixin, WinsMixin, TimeStampModification
from .validators import CodeValidator
from .querysets import HouseCustomQuerySet, DragonCustomQuerySet

# Create your models here.

class House(NameMixin, WinsMixin, TimeStampModification):
    motto = models.TextField(
        null=True,
        blank=True,
    )
    is_ruling = models.BooleanField(
        default=False,
    )
    castle = models.CharField(
        max_length=80,
        null=True,
        blank=True,
    )

    objects = HouseCustomQuerySet.as_manager()


class Dragon(NameMixin, WinsMixin, TimeStampModification):
    class Breaths(models.TextChoices):
        FIRE = 'Fire', 'Fire'
        ICE = 'Ice', 'Ice'
        LIGHTNING = 'Lightning', 'Lightning'
        UNKNOWN = 'Unknown', 'Unknown'

    power = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(Decimal("1.0")),
            MaxValueValidator(Decimal("10.0")),
        ],
        default=Decimal("1.0"),
    )
    breath = models.CharField(
        max_length=9,
        default='Unknown',
        choices=Breaths.choices,
    )
    is_healthy = models.BooleanField(
        default=True,
    )
    birth_date = models.DateField(
        default=date.today,
    )
    house = models.ForeignKey(
        to='House',
        on_delete=models.CASCADE,
        related_name='dragons',
    )

    objects = DragonCustomQuerySet.as_manager()


class Quest(NameMixin, TimeStampModification):
    code = models.CharField(
        max_length=4,
        validators=[
            MinLengthValidator(4),
            CodeValidator(),
        ],
        unique=True,
    )
    reward = models.FloatField(
        default=100.0,
    )
    start_time = models.DateTimeField()
    dragons = models.ManyToManyField(
        to='Dragon',
        related_name='quests'
    )
    host = models.ForeignKey(
        to='House',
        on_delete=models.CASCADE,
        related_name='quests',
    )