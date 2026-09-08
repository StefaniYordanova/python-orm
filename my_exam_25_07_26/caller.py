import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Publisher, Author, Book
from django.db.models import Q, Count, Avg, F, Case, When
from decimal import Decimal


# Create queries within functions
def populate_db():
    publisher1 = Publisher.objects.create(
        name='Publisher 1',
        country='Country 1',
    )
    publisher2 = Publisher.objects.create(
        name='Publisher 2',
        country='Country 2',
    )

    author1 = Author.objects.create(
        name='Author 1',
        country='Country 1'
    )
    author2 = Author.objects.create(
        name='Author 2',
        country='Country 2'
    )

    book1 = Book.objects.create(
        title='Title 1',
        publication_date='2023-01-01',
        publisher=publisher1,
        main_author=author1,
    )
    book2 = Book.objects.create(
        title='Title 2',
        publication_date='2024-01-01',
        publisher=publisher2,
        main_author=author2,
    )

    book1.co_authors.add(author2)
    book2.co_authors.add(author1)



def get_publishers(search_string=None) -> str:
    if search_string is None:
        return "No search criteria."

    publishers = Publisher.objects.filter(
        Q(name__icontains=search_string) |
        Q(country__icontains=search_string)
    ).order_by('-rating', 'name')

    if not publishers:
        return "No publishers found."

    return '\n'.join(
        f"Publisher: {p.name}, country: {'Unknown' if p.country == 'TBC' else p.country}, "
        f"rating: {p.rating:.1f}"
        for p in publishers
    )

def get_top_publisher() -> str:
    publisher = Publisher.objects.get_publishers_by_books_count().first()

    if not publisher:
        return "No publishers found."

    return f"Top Publisher: {publisher.name} with {publisher.number_of_books} books."

def get_top_main_author() -> str:
    author = Author.objects.annotate(
        number_of_books=Count('written_books'),
    ).order_by('-number_of_books', 'name').first()

    if not author or author.number_of_books == 0:
        return "No results."

    books_titles = ', '.join(
        b.title for b in author.written_books.order_by('title')
    )
    avg_rating = author.written_books.aggregate(
        average=Avg('rating'),
    )['average']

    return (f"Top Author: {author.name}, "
            f"own book titles: {books_titles}, "
            f"books average rating: {avg_rating:.1f}")





def get_authors_by_books_count() -> str:
    authors = Author.objects.annotate(
        number_of_books=Count('written_books') + Count('books'),
    ).order_by('number_of_books', 'name')

    if not authors or authors[0].number_of_books == 0:
        return "No results."

    if authors.count() > 3:
        authors = authors[:3]

    return '\n'.join(
        f"{a.name} authored {a.number_of_books} books."
        for a in authors
    )

def get_bestseller() -> str:
    book = Book.objects.select_related('main_author').prefetch_related('co_authors').filter(
        is_bestseller=True
    ).annotate(
        number_of_authors=Count('co_authors') + 1,
    ).annotate(
        composite_index=F('rating') + F('number_of_authors'),
    ).order_by(
        '-composite_index',
        '-rating',
        '-number_of_authors',
        'title',
    ).first()

    if not book:
        return "No results."

    co_authors = '/'.join(
        a.name for a in book.co_authors.order_by('name')
    ) if book.co_authors.all() else 'N/A'

    return (f"Top bestseller: {book.title}, "
            f"index: {book.composite_index}. "
            f"Main author: {book.main_author.name}. "
            f"Co-authors: {co_authors}.")

def increase_price() -> str:
    books_to_be_updated = Book.objects.select_related('publisher').annotate(
        sum_of_ratings=F('rating') + F('publisher__rating'),
    ).filter(
        publication_date__year=2025,
        sum_of_ratings__gte=8.0,
    )

    updated_books = books_to_be_updated.update(
        price=Case(
            When(
                price__gt=Decimal('50.00'),
                then=F('price') * Decimal('1.10'),
            ),
            default=F('price') * Decimal('1.20'),
        )
    )

    if updated_books == 0:
        return "No changes in price."

    return f"Prices increased for {updated_books} book/s."