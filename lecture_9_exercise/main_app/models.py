from django.db import models
from django.db.models import QuerySet, Count, Avg, F, Q
from datetime import timedelta
from decimal import Decimal
from .validators import RatingValidator, ReleaseYearValidator


# Create your models here.
class RealEstateListingManager(models.Manager):
    def by_property_type(self, property_type: str) -> QuerySet:
        return self.filter(property_type=property_type)

    def in_price_range(self, min_price: Decimal, max_price: Decimal) -> QuerySet:
        return self.filter(price__range=(min_price, max_price))

    def with_bedrooms(self, bedrooms_count: int) -> QuerySet:
        return self.filter(bedrooms=bedrooms_count)

    def popular_locations(self) -> QuerySet:
        return (
            self.values('location')
            .annotate(location_count=Count('location'))
            .order_by('-location_count')[:2]
        )


class RealEstateListing(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('House', 'House'),
        ('Flat', 'Flat'),
        ('Villa', 'Villa'),
        ('Cottage', 'Cottage'),
        ('Studio', 'Studio'),
    ]

    property_type = models.CharField(max_length=100, choices=PROPERTY_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    location = models.CharField(max_length=100)

    objects = RealEstateListingManager()


class VideoGameManager(models.Manager):
    def games_by_genre(self, genre: str) -> QuerySet:
        return self.filter(genre=genre)

    def recently_released_games(self, year: int) -> QuerySet:
        return self.filter(release_year__gte=year)

    def highest_rated_game(self):
        return self.order_by('-rating').first()

    def lowest_rated_game(self):
        return self.order_by('rating').first()

    def average_rating(self):
        avg = self.aggregate(
        avg_rating = Avg('rating'),
        )
        return f"{avg['avg_rating']:.1f}"


class VideoGame(models.Model):
    GENRE_CHOICES = [
        ('Action', 'Action'),
        ('RPG', 'RPG'),
        ('Adventure', 'Adventure'),
        ('Sports', 'Sports'),
        ('Strategy', 'Strategy'),
    ]

    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
    release_year = models.PositiveIntegerField(
        validators=[
            ReleaseYearValidator(),
        ]
    )
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[
            RatingValidator(),
        ]
    )

    def __str__(self):
        return self.title

    objects = VideoGameManager()


class BillingInfo(models.Model):
    address = models.CharField(max_length=200)


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True)
    billing_info = models.OneToOneField(BillingInfo, on_delete=models.CASCADE)

    @staticmethod
    def get_invoices_with_prefix(prefix: str) -> QuerySet:
        return Invoice.objects.filter(invoice_number__startswith=prefix)

    @staticmethod
    def get_invoices_sorted_by_number() -> QuerySet:
        return Invoice.objects.order_by('invoice_number')

    @classmethod
    def get_invoice_with_billing_info(cls, invoice_number: str) -> 'Invoice':
        return cls.objects.get(invoice_number=invoice_number)


class Technology(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    technologies_used = models.ManyToManyField(Technology, related_name='projects')

    @staticmethod
    def get_programmers_with_technologies() -> QuerySet:
        return Programmer.objects.prefetch_related('projects__technologies_used')


class Programmer(models.Model):
    name = models.CharField(max_length=100)
    projects = models.ManyToManyField(Project, related_name='programmers')

    def get_projects_with_technologies(self) -> QuerySet:
        return self.projects.prefetch_related("technologies_used")


class Task(models.Model):
    PRIORITIES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITIES)
    is_completed = models.BooleanField(default=False)
    creation_date = models.DateField()
    completion_date = models.DateField()

    @staticmethod
    def ongoing_high_priority_tasks() -> QuerySet:
        return Task.objects.filter(priority='High', is_completed=False, completion_date__gt=F('creation_date'))

    @staticmethod
    def completed_mid_priority_tasks() -> QuerySet:
        return Task.objects.filter(priority='Medium', is_completed=True)

    @staticmethod
    def search_tasks(query: str) -> QuerySet:
        condition = Q(title__icontains=query) | Q(description__icontains=query)
        return Task.objects.filter(condition)

    @staticmethod
    def recent_completed_tasks(days: int) -> QuerySet:
        return Task.objects.filter(is_completed=True, completion_date__gte=F('creation_date') - timedelta(days=days))


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    difficulty_level = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()
    repetitions = models.PositiveIntegerField()

    @staticmethod
    def get_long_and_hard_exercises() -> QuerySet:
        return Exercise.objects.filter(duration_minutes__gt=30, difficulty_level__gte=10)

    @staticmethod
    def get_short_and_easy_exercises() -> QuerySet:
        return Exercise.objects.filter(duration_minutes__lt=15, difficulty_level__lt=5)

    @staticmethod
    def get_exercises_within_duration(min_duration: int, max_duration: int) -> QuerySet:
        return Exercise.objects.filter(duration_minutes__range=(min_duration, max_duration))

    @staticmethod
    def get_exercises_with_difficulty_and_repetitions(min_difficulty: int, min_repetitions: int) -> QuerySet:
        return Exercise.objects.filter(
            difficulty_level__gte=min_difficulty,
            repetitions__gte=min_repetitions,
        )

