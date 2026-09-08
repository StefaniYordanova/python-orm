from django.db.models import QuerySet
from django.db.models.aggregates import Count


class ProfileCustomQuerySet(QuerySet):
    def get_regular_customers(self) -> QuerySet:
        return self.annotate(
            number_of_orders=Count('orders'),
        ).filter(number_of_orders__gt=2).order_by(
            '-number_of_orders',
        )



class ProductCustomQuerySet(QuerySet):
    def get_products_by_orders_count(self) -> QuerySet:
        return self.annotate(
            number_of_orders=Count('orders'),
        ).order_by('-number_of_orders', 'name')

