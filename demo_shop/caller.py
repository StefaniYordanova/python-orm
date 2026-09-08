import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo_shop.settings")
django.setup()

# Import your models here
from main_app.models import Customers
from main_app.models import Addresses

