from django.db.models import QuerySet, Count


class DirectorCustomQuerySet(QuerySet):
    def get_directors_by_movies_count(self) -> QuerySet:
        return self.annotate(
            number_of_movies=Count('directed_movies'),
        ).order_by('-number_of_movies', 'full_name')


class ActorCustomQuerySet(QuerySet):
    def get_actors_by_starred_movies_count(self) -> QuerySet:
        return self.annotate(
            number_of_starred_movies=Count('starred_movies'),
        ).order_by('-number_of_starred_movies', 'full_name')

    def get_actors_by_participated_movies_count(self) -> QuerySet:
        return self.annotate(
            num_of_participated_movies=Count('participated_movies'),
        ).order_by('-num_of_participated_movies', 'full_name')
