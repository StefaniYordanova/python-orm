from decimal import Decimal

from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from main_app.mixins import PersonalInfoMixin, RatingMixin, TimeStampUpdatedMixin
from main_app.querysets import PublisherCustomQuerySet

# Create your models here.

class Publisher(PersonalInfoMixin, RatingMixin):
    established_date = models.DateField(
        default='1800-01-01',
    )

    objects = PublisherCustomQuerySet.as_manager()


class Author(PersonalInfoMixin, TimeStampUpdatedMixin):
    birth_date = models.DateField(
        null=True, blank=True,
    )
    is_active = models.BooleanField(
        default=True,
    )


class Book(RatingMixin, TimeStampUpdatedMixin):

    class Genres(models.TextChoices):
        FICTION = 'Fiction', 'Fiction'
        NON_FICTION = 'Non-Fiction', 'Non-Fiction'
        OTHER = 'Other', 'Other'

    title = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(2),
        ]
    )
    publication_date = models.DateField()
    summary = models.TextField(
        null=True, blank=True,
    )
    genre = models.CharField(
        max_length=11,
        default='Other',
        choices=Genres.choices,
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal("0.01"),
        validators=[
            MinValueValidator(Decimal("0.01")),
            MaxValueValidator(Decimal("9999.99")),
        ]
    )
    is_bestseller = models.BooleanField(default=False)
    publisher = models.ForeignKey(
        to='Publisher',
        on_delete=models.CASCADE,
        related_name='published_books',
    )
    main_author = models.ForeignKey(
        to='Author',
        on_delete=models.CASCADE,
        related_name='written_books',
    )
    co_authors = models.ManyToManyField(
        to='Author',
        related_name='books',
    )

