from django.db.models import QuerySet
from django.db.models.aggregates import Count


class PublisherCustomQuerySet(QuerySet):
    def get_publishers_by_books_count(self) -> QuerySet:
        return self.annotate(
            number_of_books=Count('published_books'),
        ).order_by('-number_of_books', 'name')
