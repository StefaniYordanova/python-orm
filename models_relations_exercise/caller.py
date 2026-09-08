import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import QuerySet
from main_app.models import Author, Artist, Song, Product, Review, DrivingLicense, Driver, Owner, Registration, Car
from datetime import timedelta
from datetime import date


# Create queries within functions
def show_all_authors_with_their_books() -> str:
    result = []
    authors = Author.objects.all()
    for a in authors:
        if a.book_set.all():
            result.append(f"{a.name} has written - "
                          f"{', '.join(b.title for b in a.book_set.all())}!")
    return '\n'.join(result)


def delete_all_authors_without_books() -> None:
    authors = Author.objects.all()
    for a in authors:
        if a.book_set.exists():
            Author.objects.filter(id=a.id).delete()


# authors_with_books = show_all_authors_with_their_books()
# print(authors_with_books)
# print(Author.objects.count())

def add_song_to_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.add(song)


def get_songs_by_artist(artist_name: str) -> QuerySet:
    artist = Artist.objects.get(name=artist_name)
    return artist.songs.all().order_by('-id')


def remove_song_from_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.remove(song)


def calculate_average_rating_for_product_by_name(product_name: str) -> float:
    product = Product.objects.get(name=product_name)
    avg_rating = sum(r.rating for r in product.reviews.all()) / len(product.reviews.all())
    return avg_rating


def get_reviews_with_high_ratings(threshold: int) -> QuerySet:
    return Review.objects.filter(rating__gte=threshold)


def get_products_with_no_reviews() -> QuerySet:
    return Product.objects.filter(reviews__isnull=True).order_by('-name')


def delete_products_without_reviews() -> None:
    Product.objects.filter(reviews__isnull=True).delete()


def calculate_licenses_expiration_dates() -> str:
    result = []
    for l in DrivingLicense.objects.all().order_by('-license_number'):
        result.append(f"License with number: {l.license_number} "
                      f"expires on {l.issue_date + timedelta(days=365)}!")
    return '\n'.join(result)


def get_drivers_with_expired_licenses(due_date: date) -> QuerySet:
    return Driver.objects.filter(license__issue_date__lt=due_date - timedelta(days=365))


# expiration_dates = calculate_licenses_expiration_dates()
# print(expiration_dates)
#
# drivers_with_expired_licenses = get_drivers_with_expired_licenses(date(2023, 1, 1))
# for driver in drivers_with_expired_licenses:
#     print(f"{driver.first_name} {driver.last_name} has to renew their driving license!")

def register_car_by_owner(owner: Owner) -> str:
    registration = Registration.objects.filter(car__isnull=True).first()
    car = Car.objects.filter(registration__isnull=True).first()

    registration.car = car
    registration.registration_date = date.today()
    registration.save()

    car.owner = owner
    car.save()

    return (f"Successfully registered {car.model} to "
            f"{owner.name} with registration number {registration.registration_number}.")

