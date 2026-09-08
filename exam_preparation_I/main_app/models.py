from decimal import Decimal

from django.core.validators import MinValueValidator, MinLengthValidator, MaxValueValidator
from django.db import models
from .mixins import PersonalInfoMixin, AwardedMixin, TimeStampUpdateMixin
from .querysets import DirectorCustomQuerySet, ActorCustomQuerySet

# Create your models here.

class Director(PersonalInfoMixin):
    years_of_experience = models.SmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
        ]
    )

    objects = DirectorCustomQuerySet.as_manager()


class Actor(PersonalInfoMixin, AwardedMixin, TimeStampUpdateMixin):
    objects = ActorCustomQuerySet.as_manager()


class Movie(AwardedMixin, TimeStampUpdateMixin):
    class Genres(models.TextChoices):
        ACTION = 'Action', 'Action'
        COMEDY = 'Comedy', 'Comedy'
        DRAMA = 'Drama', 'Drama'
        OTHER = 'Other', 'Other'

    title = models.CharField(
        max_length=150,
        validators=[
            MinLengthValidator(5),
        ]
    )
    release_date = models.DateField()
    storyline = models.TextField(
        null=True,
        blank=True,
    )
    genre = models.CharField(
        max_length=6,
        default='Other',
        choices=Genres.choices,
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(Decimal("0.0")),
            MaxValueValidator(Decimal("10.0")),
        ],
        default=Decimal("0.0"),
    )
    is_classic = models.BooleanField(
        default=False,
    )
    director = models.ForeignKey(
        to='Director',
        on_delete=models.CASCADE,
        related_name='directed_movies',
    )
    starring_actor = models.ForeignKey(
        to='Actor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='starred_movies',
    )
    actors = models.ManyToManyField(
        to='Actor',
        related_name='participated_movies',
    )