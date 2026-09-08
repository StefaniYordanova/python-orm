import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Customer, Book, SpiderHero, FlashHero
from django.core.exceptions import ValidationError

spiderman = SpiderHero(name="Spider-Man", hero_title="Spider Hero", energy=100)
flash = FlashHero(name="The Flash", hero_title="Flash Hero", energy=70)
spiderman.save()

flash.save()

print(spiderman.swing_from_buildings())
print(flash.run_at_super_speed())
print(spiderman.swing_from_buildings())

spiderman.recharge_energy(195)

flash.recharge_energy(40)

print(f"{spiderman.name} - Energy: {spiderman.energy}")
print(f"{flash.name} - Energy: {flash.energy}")