import os
import django

from main_app.mixins import WinsMixin

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import House, Dragon, Quest
from django.db.models import Q, F, Min, Avg
from decimal import Decimal

# Create queries within functions

def get_houses(search_string=None) -> str:
    if not search_string:
        return "No houses match your search."

    houses = House.objects.filter(
        Q(name__istartswith=search_string) |
        Q(motto__istartswith=search_string)
    ).order_by('-wins', 'name')

    if not houses:
        return "No houses match your search."

    return '\n'.join(
        f"House: {h.name}, "
        f"wins: {h.wins}, "
        f"motto: {h.motto if h.motto else 'N/A'}"
        for h in houses
    )

def get_most_dangerous_house() -> str:
    house = House.objects.get_houses_by_dragons_count().first()

    if not house or house.number_of_dragons == 0:
        return "No relevant data."

    ruling = 'ruling' if house.is_ruling else 'not ruling'

    return (f"The most dangerous house is the House of {house.name} "
            f"with {house.number_of_dragons} dragons. "
            f"Currently {ruling} the kingdom.")

def get_most_powerful_dragon() -> str:
    dragon = Dragon.objects.select_related('house').prefetch_related('quests').get_powerful_dragons().first()

    if not dragon:
        return "No relevant data."

    return (f"The most powerful healthy dragon is {dragon.name} "
            f"with a power level of {dragon.power:.1f}, "
            f"breath type {dragon.breath}, and {dragon.wins} wins, "
            f"coming from the house of {dragon.house.name}. "
            f"Currently participating in {dragon.quests.count()} quests.")






def update_dragons_data() -> str:
    updated_dragons = Dragon.objects.filter(
        is_healthy=False,
        power__gte=Decimal("1.1"),
    ).update(
        power=F('power') - Decimal("0.1"),
        is_healthy=True,
    )

    if updated_dragons == 0:
        return "No changes in dragons data."

    min_power = Dragon.objects.aggregate(
        min_power_level=Min('power'),
    )['min_power_level']

    return (f"The data for {updated_dragons} dragon/s has "
            f"been changed. The minimum power level "
            f"among all dragons is {min_power:.1f}")

def get_earliest_quest() -> str:
    quest = Quest.objects.select_related('host').prefetch_related('dragons').order_by('start_time').first()

    if not quest:
        return "No relevant data."

    dragons = '*'.join(
        d.name for d in quest.dragons.order_by('-power', 'name')
    )
    avg_power_level = quest.dragons.aggregate(
        avg_power=Avg('power'),
    )['avg_power']

    return (f"The earliest quest is: {quest.name}, "
            f"code: {quest.code}, "
            f"start date: {quest.start_time.day}.{quest.start_time.month}.{quest.start_time.year}, "
            f"host: {quest.host.name}. "
            f"Dragons: {dragons}. "
            f"Average dragons power level: {avg_power_level:.2f}")

def announce_quest_winner(quest_code) -> str:
    quest = Quest.objects.prefetch_related('dragons').filter(
        code__exact=quest_code,
    ).first()

    if not quest:
        return "No such quest."

    winning_dragon = quest.dragons.order_by('-power', 'name').first()
    winning_dragon.wins += 1
    winning_dragon.save()

    winning_dragon.house.wins += 1
    winning_dragon.house.save()

    result = (f"The quest: {quest.name} has been "
            f"won by dragon {winning_dragon.name} from house {winning_dragon.house.name}. "
            f"The number of wins has been "
            f"updated as follows: {winning_dragon.wins} total wins "
            f"for the dragon and {winning_dragon.house.wins} total wins for the house. "
            f"The house was awarded with {quest.reward:.2f} coins.")

    quest.delete()
    return result

