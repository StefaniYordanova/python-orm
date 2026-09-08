from django.db.models import QuerySet, Count


class HouseCustomQuerySet(QuerySet):
    def get_houses_by_dragons_count(self) -> QuerySet:
        return self.annotate(
            number_of_dragons=Count('dragons'),
        ).order_by('-number_of_dragons', 'name')


class DragonCustomQuerySet(QuerySet):
    def get_powerful_dragons(self) -> QuerySet:
        return self.filter(
            is_healthy=True,
        ).order_by('-power', 'name')

