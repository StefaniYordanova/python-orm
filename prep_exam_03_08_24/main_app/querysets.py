from django.db.models import QuerySet
from django.db.models.aggregates import Count


class AstronautCustomQuerySet(QuerySet):
    def get_astronauts_by_missions_count(self) -> QuerySet:
        return self.annotate(
            number_of_missions=Count('missions'),
        ).order_by('-number_of_missions', 'phone_number')

    def get_astronauts_by_commanded_missions_count(self) -> QuerySet:
        return self.annotate(
            num_of_commanded_missions=Count('commanded_missions'),
        ).order_by('-num_of_commanded_missions', 'phone_number')

