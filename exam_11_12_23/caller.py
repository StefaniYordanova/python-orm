import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import TennisPlayer, Tournament, Match

# Create queries within functions

def get_tennis_players(search_name=None, search_country=None) -> str:
    players = []

    if search_name and search_country:
        players = TennisPlayer.objects.filter(
            full_name__icontains=search_name,
            country__icontains=search_country,
        )

    elif search_name:
        players = TennisPlayer.objects.filter(
            full_name__icontains=search_name,
        )

    elif search_country:
        players = TennisPlayer.objects.filter(
            country__icontains=search_country,
        )

    if (search_name is None and search_country is None) or not players:
        return ''

    return '\n'.join(
        f"Tennis Player: {p.full_name}, country: {p.country}, ranking: {p.ranking}"
        for p in players.order_by('ranking')
    )

def get_top_tennis_player() -> str:
    player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()

    if not player:
        return ''

    return f"Top Tennis Player: {player.full_name} with {player.num_won_matches} wins."

def get_tennis_player_by_matches_count() -> str:
    player = TennisPlayer.objects.get_tennis_player_by_participated_matches_count().first()

    if not player or player.num_participated_matches == 0:
        return ''

    return f"Tennis Player: {player.full_name} with {player.num_participated_matches} matches played."




def get_tournaments_by_surface_type(surface=None) -> str:
    if not surface:
        return ''

    tournaments = Tournament.objects.filter(
        surface_type__icontains=surface,
    ).order_by('-start_date')

    if not tournaments:
        return ''

    return '\n'.join(
        f"Tournament: {t.name}, start date: {t.start_date}, matches: {t.matches.count()}"
        for t in tournaments
    )

def get_latest_match_info() -> str:
    match = Match.objects.select_related('winner', 'tournament').prefetch_related('players').order_by(
        '-date_played',
        '-id',
    ).first()

    if not match:
        return ''

    players_names = ' vs '.join(
        p.full_name for p in match.players.order_by('full_name')
    )
    winner = match.winner.full_name if match.winner else 'TBA'

    return (f"Latest match played on: {match.date_played}, "
            f"tournament: {match.tournament.name}, score: {match.score}, "
            f"players: {players_names}, "
            f"winner: {winner}, summary: {match.summary}")

def get_matches_by_tournament(tournament_name=None) -> str:
    if not tournament_name:
        return "No matches found."


    matches = Match.objects.select_related('winner', 'tournament').filter(
        tournament__name__exact=tournament_name,
    )

    if not matches:
        return "No matches found."

    return '\n'.join(
        f"Match played on: {m.date_played}, "
        f"score: {m.score}, "
        f"winner: {m.winner.full_name if m.winner else 'TBA'}"
        for m in matches
    )