import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Author, Book, Review

# Create and check models
def find_books_by_genre_and_language(genre, language):
    return Book.objects.filter(genre=genre, language=language)

# print(find_books_by_genre_and_language("Romance", "English"))
# print(find_books_by_genre_and_language("Poetry", "Spanish"))
# print(find_books_by_genre_and_language("Mystery", "English"))

def find_authors_nationalities():
    authors = Author.objects.exclude(nationality__isnull=True)
    return '\n'.join(f"{a.first_name} {a.last_name} is {a.nationality}" for a in authors)

# print(find_authors_nationalities())

def order_books_by_year():
    books = Book.objects.all().order_by('publication_year', 'title')
    return '\n'.join(f"{b.publication_year} year: {b.title} by {b.author}" for b in books)

# print(order_books_by_year())

def delete_review_by_id(review_id):
    review = Review.objects.get(id=review_id)
    review.delete()
    return f"Review by {review.reviewer_name} was deleted"

# print(delete_review_by_id(6))

def filter_authors_by_nationalities(nationality):
    authors = Author.objects.filter(nationality=nationality).order_by('first_name', 'last_name')
    return '\n'.join(f"{a.biography}" if a.biography else f"{a.first_name} {a.last_name}" for a in authors)

# print("American authors:")
# print(filter_authors_by_nationalities('American'))
# print()
# print("British authors:")
# print(filter_authors_by_nationalities('British'))
# print()
# print("Authors with no nationalities:")
# print(filter_authors_by_nationalities(None))

def filter_authors_by_birth_year(first_year, second_year):
    authors = Author.objects.filter(
        birth_date__year__range=(first_year, second_year)
    ).order_by('-birth_date')
    return '\n'.join(f"{a.birth_date}: {a.first_name} {a.last_name}" for a in authors)
#
# print("Authors born between 1980 and 2000:")
# print(filter_authors_by_birth_year(1980, 2000))
# print()
# print("Authors born between 1950 and 1960:")
# print(filter_authors_by_birth_year(1950, 1960))
# print()
# print("Authors born between 2000 and 2010:")
# print(filter_authors_by_birth_year(2000, 2010))

def change_reviewer_name(old_name, new_name):
    Review.objects.filter(reviewer_name=old_name).update(reviewer_name=new_name)
    return Review.objects.all()

# print("Change Alice Johnson to A.J.:")
# print(change_reviewer_name("Alice Johnson", "A.J."))
# print()
# print("Change Bob Wilson to Bobby W.:")
# print(change_reviewer_name("Bob Wilson", "Bobby W."))
# print()
# print("Change A.J. to A. Johnson:")
# print(change_reviewer_name("A.J.", "A. Johnson"))
