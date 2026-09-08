import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from datetime import date
from main_app.models import UserProfile, Message, CreditCard, Student, Hotel, SpecialReservation, Room
