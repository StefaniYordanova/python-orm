from django.db.models import QuerySet
from django.db.models.aggregates import Count, Avg


class AuthorCustomQuerySet(QuerySet):
    def get_authors_by_article_count(self) -> QuerySet:
        return self.annotate(
            number_of_articles=Count('written_articles'),
        ).order_by('-number_of_articles', 'email')

    def get_authors_by_reviews_count(self) -> QuerySet:
        return self.annotate(
            number_of_reviews=Count('reviews'),
        ).order_by('-number_of_reviews', 'email')


class ArticleCustomQuerySet(QuerySet):
    def get_articles_with_average_ratings(self) -> QuerySet:
        return self.annotate(
            avg_rating=Avg('reviews__rating'),
        ).order_by('-avg_rating', 'title')
