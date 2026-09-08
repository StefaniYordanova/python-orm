import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Astronaut, Spacecraft, Mission
from django.db.models import Q, F
from django.db.models.aggregates import Sum, Count, Avg

# Create queries within functions

def get_astronauts(search_string=None) -> str:
    if search_string is None:
        return ''

    astronauts = Astronaut.objects.filter(
        Q(name__icontains=search_string) |
        Q(phone_number__icontains=search_string)
    ).order_by('name')

    if not astronauts:
        return ''

    return '\n'.join(
        f"Astronaut: {a.name}, "
        f"phone number: {a.phone_number}, "
        f"status: {'Active' if a.is_active else 'Inactive'}"
        for a in astronauts
    )

def get_top_astronaut() -> str:
    astronaut = Astronaut.objects.get_astronauts_by_missions_count().first()

    if not astronaut or astronaut.number_of_missions == 0:
        return "No data."

    return (f"Top Astronaut: {astronaut.name} "
            f"with {astronaut.number_of_missions} missions.")

def get_top_commander() -> str:
    astronaut = Astronaut.objects.get_astronauts_by_commanded_missions_count().first()

    if not astronaut or astronaut.num_of_commanded_missions == 0:
        return "No data."

    return (f"Top Commander: {astronaut.name} with "
            f"{astronaut.num_of_commanded_missions} commanded missions.")





def get_last_completed_mission() -> str:
    mission = Mission.objects.select_related('commander', 'spacecraft').prefetch_related('astronauts').filter(
        status__exact='Completed',
    ).order_by('-launch_date').first()

    if not mission:
        return "No data."

    commander_name = mission.commander.name if mission.commander else 'TBA'
    astronauts_names = ', '.join(
        a.name for a in mission.astronauts.order_by('name')
    )
    total_spacewalks = mission.astronauts.aggregate(
        total=Sum('spacewalks'),
    )['total'] or 0

    return (f"The last completed mission is: {mission.name}. "
            f"Commander: {commander_name}. "
            f"Astronauts: {astronauts_names}. "
            f"Spacecraft: {mission.spacecraft.name}. "
            f"Total spacewalks: {total_spacewalks}.")

def get_most_used_spacecraft() -> str:
    spacecraft = Spacecraft.objects.annotate(
        number_of_missions=Count('missions'),
        number_of_astronauts=Count('missions__astronauts', distinct=True,),
    ).order_by('-number_of_missions', 'name').first()

    if not spacecraft or spacecraft.number_of_missions == 0:
        return "No data."

    return (f"The most used spacecraft is: {spacecraft.name}, "
            f"manufactured by {spacecraft.manufacturer}, "
            f"used in {spacecraft.number_of_missions} missions, "
            f"astronauts on missions: {spacecraft.number_of_astronauts}.")

def decrease_spacecrafts_weight():
    spacecrafts_updated = Spacecraft.objects.filter(
        missions__status='Planned',
        weight__gte=200.0,
    ).update(
        weight=F('weight') - 200.0,
    )

    if spacecrafts_updated == 0:
        return "No changes in weight."

    avg_weight = Spacecraft.objects.aggregate(
        avg=Avg('weight'),
    )['avg']

    return (f"The weight of {spacecrafts_updated} spacecrafts "
            f"has been decreased. The new average weight "
            f"of all spacecrafts is {avg_weight:.1f}kg")
