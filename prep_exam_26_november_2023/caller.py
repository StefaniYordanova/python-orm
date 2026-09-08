import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Article, Review
from django.db.models.aggregates import Avg, Count


# Create queries within functions

def get_authors(search_name=None, search_email=None) -> str:
    authors = []

    if search_name and search_email:
        authors = Author.objects.filter(
            full_name__icontains=search_name,
            email__icontains=search_email,
        )

    elif search_name:
        authors = Author.objects.filter(
            full_name__icontains=search_name,
        )

    elif search_email:
        authors = Author.objects.filter(
            email__icontains=search_email,
        )

    if (search_name is None and search_email is None) or not authors:
        return ''

    return '\n'.join(
        f"Author: {a.full_name}, "
        f"email: {a.email}, "
        f"status: {'Banned' if a.is_banned else 'Not Banned'}"
        for a in authors.order_by('-full_name')
    )

def get_top_publisher() -> str:
    author = Author.objects.get_authors_by_article_count().first()

    if not author or author.number_of_articles == 0:
        return ''

    return f"Top Author: {author.full_name} with {author.number_of_articles} published articles."

def get_top_reviewer() -> str:
    author = Author.objects.get_authors_by_reviews_count().first()

    if not author or author.number_of_reviews == 0:
        return ''

    return f"Top Reviewer: {author.full_name} with {author.number_of_reviews} published reviews."





def get_latest_article() -> str:
    article = Article.objects.prefetch_related('reviews').order_by('published_on').last()

    if not article:
        return ''

    authors_names = ', '.join(
        a.full_name for a in article.authors.order_by('full_name')
    )

    num_reviews = article.reviews.count()

    avg_rating = article.reviews.aggregate(
        average_rating=Avg('rating'),
    )['average_rating'] or 0

    return (f"The latest article is: {article.title}. "
            f"Authors: {authors_names}. "
            f"Reviewed: {num_reviews} times. "
            f"Average Rating: {avg_rating:.2f}.")

def get_top_rated_article() -> str:
    article = (Article.objects.get_articles_with_average_ratings()
               .prefetch_related('reviews').first())

    if not article or article.avg_rating is None:
        return ''

    return (f"The top-rated article is: {article.title}, "
            f"with an average rating of {article.avg_rating:.2f}, "
            f"reviewed {article.reviews.count()} times.")

def ban_author(email=None) -> str:
    author: 'Author' = None

    if email:
        author = Author.objects.filter(
            email__exact=email,
        )

    if not email or not author:
        return 'No authors banned.'

    author.is_banned = True
    author.save()

    deleted_reviews = author.reviews.all().delete()

    return f"Author: {author.full_name} is banned! {deleted_reviews} reviews deleted."

