from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from django.db import models
from main_app.mixins import ContentMixin, TimeStampPublishedMixin
from main_app.querysets import AuthorCustomQuerySet, ArticleCustomQuerySet

# Create your models here.

class Author(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3),
        ]
    )
    email = models.EmailField(unique=True)
    is_banned = models.BooleanField(default=False)
    birth_year = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(2005),
            MinValueValidator(1900),
        ]
    )
    website = models.URLField(
        null=True,
        blank=True,
    )

    objects = AuthorCustomQuerySet.as_manager()


class Article(ContentMixin, TimeStampPublishedMixin):

    class Categories(models.TextChoices):
        TECHNOLOGY = 'Technology', 'Technology'
        SCIENCE = 'Science', 'Science'
        EDUCATION = 'Education', 'Education'

    title = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(5),
        ]
    )
    category = models.CharField(
        max_length=10,
        default='Technology',
        choices=Categories.choices,
    )
    authors = models.ManyToManyField(
        to='Author',
        related_name='written_articles',
    )

    objects = ArticleCustomQuerySet.as_manager()


class Review(ContentMixin, TimeStampPublishedMixin):
    rating = models.FloatField(
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(5.0),
        ]
    )
    author = models.ForeignKey(
        to='Author',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    article = models.ForeignKey(
        to='Article',
        on_delete=models.CASCADE,
        related_name='reviews',
    )

