import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Director, Actor, Movie
from django.db.models import Q, Avg, F
from decimal import Decimal

# Create queries within functions

def populate_db() -> None:
    director1 = Director.objects.create(
        full_name='Director 1',
    )
    director2 = Director.objects.create(
        full_name='Director 2',
    )

    actor1 = Actor.objects.create(
        full_name='Actor 1',
    )
    actor2 = Actor.objects.create(
        full_name='Actor 2',
    )

    movie1 = Movie.objects.create(
        title='Title 1',
        release_date='2023-01-01',
        director=director1,
        starring_actor=actor1,
    )
    movie2 = Movie.objects.create(
        title='Title 2',
        release_date='2025-01-01',
        director=director2,
        starring_actor=actor2,
    )

    movie1.actors.add(actor2)
    movie2.actors.add(actor1)



def get_directors(search_name=None, search_nationality=None) -> str:
    directors = []

    if search_name and search_nationality:
        directors = Director.objects.filter(
            Q(full_name__icontains=search_name) &
            Q(nationality__icontains=search_nationality)
        )

    elif search_name:
        directors = Director.objects.filter(
            full_name__icontains=search_name,
        )

    elif search_nationality:
        directors = Director.objects.filter(
            nationality__icontains=search_nationality,
        )

    if (search_name is None and search_nationality is None) or not directors:
        return ''

    return '\n'.join(
        f"Director: {d.full_name}, "
        f"nationality: {d.nationality}, "
        f"experience: {d.years_of_experience}"
        for d in directors.order_by('full_name')
    )

def get_top_director() -> str:
    director = Director.objects.get_directors_by_movies_count().first()

    if not director:
        return ''

    return f"Top Director: {director.full_name}, movies: {director.number_of_movies}."

def get_top_actor() -> str:
    actor = Actor.objects.get_actors_by_starred_movies_count().first()

    if not actor or actor.number_of_starred_movies == 0:
        return ''

    movie_titles = ', '.join(
        m.title for m in actor.starred_movies.all()
    )
    avg_rating = actor.starred_movies.aggregate(
        avg=Avg('rating'),
    )['avg']

    return (f"Top Actor: {actor.full_name}, "
            f"starring in movies: {movie_titles}, "
            f"movies average rating: {avg_rating:.1f}")






def get_actors_by_movies_count() -> str:
    actors = Actor.objects.get_actors_by_participated_movies_count()

    if not actors or actors[0].num_of_participated_movies == 0:
        return ''

    if actors.count() > 3:
        actors = actors[:3]

    return '\n'.join(
        f"{a.full_name}, participated in {a.num_of_participated_movies} movies"
        for a in actors
    )

def get_top_rated_awarded_movie() -> str:
    movie = Movie.objects.select_related('starring_actor').prefetch_related('actors').filter(
        is_awarded=True,
    ).order_by('-rating', 'title').first()

    if not movie:
        return ''

    starring_actor = movie.starring_actor.full_name if movie.starring_actor else 'N/A'
    cast = ', '.join(
        a.full_name for a in movie.actors.order_by('full_name')
    )

    return (f"Top rated awarded movie: {movie.title}, "
            f"rating: {movie.rating:.1f}. "
            f"Starring actor: {starring_actor}. "
            f"Cast: {cast}.")

def increase_rating() -> str:
    updated_movies = Movie.objects.filter(
        is_classic=True,
        rating__lte=Decimal("9.9"),
    ).update(
        rating=F('rating') + Decimal("0.1"),
    )

    if updated_movies == 0:
        return "No ratings increased."

    return f"Rating increased for {updated_movies} movies."

