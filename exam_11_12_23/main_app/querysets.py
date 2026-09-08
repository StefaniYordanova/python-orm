from django.db.models import QuerySet
from django.db.models.aggregates import Count


class TennisPlayerCustomQuerySet(QuerySet):
    def get_tennis_players_by_wins_count(self) -> QuerySet:
        return self.annotate(
            num_won_matches=Count('won_matches'),
        ).order_by('-num_won_matches', 'full_name')

    def get_tennis_player_by_participated_matches_count(self) -> QuerySet:
        return self.annotate(
            num_participated_matches=Count('participated_matches'),
        ).order_by('-num_participated_matches', 'ranking')
