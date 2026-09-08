import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from decimal import Decimal
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


# Create queries within functions

def create_pet(name: str, species: str):
    Pet.objects.create(name=name, species=species)
    return f"{name} is a very cute {species}!"


# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))

def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    Artifact.objects.create(name=name, origin=origin, age=age, description=description, is_magical=is_magical)
    return f"The artifact {name} is {age} years old!"


def rename_artifact(artifact: Artifact, new_name: str):
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts():
    Artifact.objects.all().delete()


# print(create_artifact('Ancient Sword', 'Lost Kingdom', 500, 'A legendary sword with a rich history', True))
# artifact_object = Artifact.objects.get(name='Ancient Sword')
# rename_artifact(artifact_object, 'Ancient Shield')
# print(artifact_object.name)

def show_all_locations():
    locations = Location.objects.all().order_by('-id')
    result = []
    for location in locations:
        result.append(f'{location.name} has a population of {location.population}!')

    return '\n'.join(result)


def new_capital():
    first_location = Location.objects.first()
    if first_location:
        first_location.is_capital = True
        first_location.save()


def get_capitals():
    return Location.objects.all().filter(is_capital=True).values("name")


def delete_first_location():
    Location.objects.first().delete()


# Location.objects.create(
#     name='Sofia',
#     region='Sofia Region',
#     population=1329000,
#     description='The capital of Bulgaria and the largest city in the country',
#     is_capital=False,
# )
# Location.objects.create(
#     name='Plovdiv',
#     region='Plovdiv Region',
#     population=346942,
#     description='The second-largest city in Bulgaria with a rich historical heritage',
#     is_capital=False,
# )
# Location.objects.create(
#     name='Varna',
#     region='Varna Region',
#     population=330486,
#     description='A city known for its sea breeze and beautiful beaches on the Black Sea',
#     is_capital=False,
# )
#
# print(show_all_locations())
# print(new_capital())
# print(get_capitals())

def apply_discount():
    cars = Car.objects.all()

    for c in cars:
        discount_percentage = sum(int(d) for d in str(c.year))

        c.price_with_discount = c.price * (Decimal('1') - Decimal(discount_percentage) / Decimal('100'))

    Car.objects.bulk_update(cars, ['price_with_discount'])


def get_recent_cars():
    return Car.objects.all().filter(year__gt=2020).values("model", "price_with_discount")


def delete_last_car():
    Car.objects.last().delete()


# Car.objects.create(
#     model='Mercedes C63 AMG',
#     year=2019,
#     color='white',
#     price=120000.00
# )
# Car.objects.create(
#     model='Audi Q7 S line',
#     year=2023,
#     color='black',
#     price=183900.00
# )
# Car.objects.create(
#     model='Chevrolet Corvette',
#     year=2021,
#     color='dark grey',
#     price=199999.00
# )
#
# apply_discount()
# print(get_recent_cars())

def show_unfinished_tasks():
    result = []
    for t in Task.objects.all().filter(is_finished=False):
        result.append(f"Task - {t.title} needs to be done until {t.due_date}!")
    return '\n'.join(result)


def complete_odd_tasks():
    tasks = Task.objects.all()

    for t in odd_tasks:
        if t.id % 2 != 0 and not t.is_finished:
            t.is_finished = True

    Task.objects.bulk_update(tasks, ['is_finished'])


def encode_and_replace(text: str, task_title: str):
    tasks = Task.objects.all().filter(title=task_title)
    new_text = ''
    for letter in text:
        new_text += chr(ord(letter) - 3)

    for t in tasks:
        t.description = new_text
    Task.objects.bulk_update(tasks, ['description'])


# Task.objects.create(
#     title="Sample Task",
#     description="This is a sample task description",
#     due_date='2023-10-31',
#     is_finished=False
# )

# encode_and_replace("Zdvk#wkh#glvkhv$", "Sample Task")
# print(Task.objects.get(title='Sample Task').description)

def get_deluxe_rooms():
    rooms = HotelRoom.objects.all().filter(room_type="Deluxe")
    result = []
    for r in rooms:
        if r.id % 2 == 0:
            result.append(f"Deluxe room with number {r.room_number} costs {r.price_per_night}$ per night!")

    return '\n'.join(result)


def increase_room_capacity():
    rooms = HotelRoom.objects.all().order_by("id")
    for i in range(len(rooms)):
        if not rooms[i].is_reserved:
            continue
        if i == 1:
            rooms[i].capacity += rooms[i].id
        else:
            rooms[i].capacity += rooms[i - 1].capacity

    HotelRoom.objects.bulk_update(rooms, ['capacity'])


def reserve_first_room():
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()


def delete_last_room():
    last_room = HotelRoom.objects.last()
    if not last_room.is_reserved:
        HotelRoom.objects.last().delete()


# HotelRoom.objects.create(
#     room_number=401,
#     room_type="Standard",
#     capacity=2,
#     amenities="tv",
#     price_per_night=100.00,
# )
#
# HotelRoom.objects.create(
#     room_number=501,
#     room_type="Deluxe",
#     capacity=3,
#     amenities="Wi-Fi",
#     price_per_night=200.00,
# )
#
# HotelRoom.objects.create(
#     room_number=601,
#     room_type="Deluxe",
#     capacity=6,
#     amenities="Jacuzzi",
#     price_per_night=400.00,
# )

# print(get_deluxe_rooms())
# reserve_first_room()
# print(HotelRoom.objects.get(room_number=401).is_reserved)

def update_characters():
    characters = Character.objects.all()
    for c in characters:
        if c.class_name == "Mage":
            c.level += 3
            c.intelligence -= 7
        elif c.class_name == "Warrior":
            c.hit_points //= 2
            c.dexterity += 4
        elif c.class_name == "Assassin" or c.class_name == "Scout":
            c.inventory = "The inventory is empty"

    Character.objects.bulk_create(characters, ["level", "intelligence", "hit_points", "dexterity", "inventory"])


def fuse_characters(first_character: Character, second_character: Character):
    new_name = f"{first_character.name} {second_character.name}"
    new_level = (first_character.level + second_character.level) // 2
    new_strength = (first_character.strength + second_character.strength) * 1.2
    new_dexterity = (first_character.dexterity + second_character.dexterity) * 1.4
    new_intelligence = (first_character.intelligence + second_character.intelligence) * 1.5
    new_hit_points = first_character.hit_points + second_character.hit_points
    new_inventory = ''
    if first_character.class_name == "Mage" or first_character.class_name == "Scout":
        new_inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    elif first_character.class_name == "Warrior" or first_character.class_name == "Assassin":
        new_inventory = "Dragon Scale Armor, Excalibur"

    Character.objects.filter(id=first_character.id).delete()
    Character.objects.filter(id=second_character.id).delete()
    Character.objects.create(
        name=new_name,
        class_name="Fusion",
        level=new_level,
        strength=new_strength,
        dexterity=new_dexterity,
        intelligence=new_intelligence,
        hit_points=new_hit_points,
        inventory=new_inventory,
    )

def grand_dexterity():
    Character.objects.update(dexterity=30)

def grand_intelligence():
    Character.objects.update(intelligence=40)

def grand_strength():
    Character.objects.update(strength=50)

def delete_characters():
    Character.objects.filter(inventory="The inventory is empty").delete()

# character1 = Character.objects.create(
#     name='Gandalf',
#     class_name='Mage',
#     level=10,
#     strength=15,
#     dexterity=20,
#     intelligence=25,
#     hit_points=100,
#     inventory='Staff of Magic, Spellbook',
# )
#
# character2 = Character.objects.create(
#     name='Hector',
#     class_name='Warrior',
#     level=12,
#     strength=30,
#     dexterity=15,
#     intelligence=10,
#     hit_points=150,
#     inventory='Sword of Troy, Shield of Protection',
# )
# fuse_characters(character1, character2)
# fusion = Character.objects.filter(class_name='Fusion').get()
#
# print(fusion.name)
# print(fusion.class_name)
# print(fusion.level)
# print(fusion.intelligence)
# print(fusion.inventory)