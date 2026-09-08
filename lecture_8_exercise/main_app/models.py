from abc import abstractmethod

from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models
from .validators import validate_customer_name, validate_customer_phone_number
from decimal import Decimal

# Create your models here.

class Customer(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            validate_customer_name
        ],
    )
    age = models.PositiveIntegerField(
        validators=[
            MinValueValidator(18, message="Age must be greater than or equal to 18"),
        ]
    )
    email = models.EmailField(
        error_messages={
            "invalid": "Enter a valid email address"
        }
    )
    phone_number = models.CharField(
        max_length=13,
        validators=[
            validate_customer_phone_number
        ]
    )
    website_url = models.URLField(
        error_messages={
            "invalid": "Enter a valid URL"
        }
    )



class BaseMedia(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', 'title']

class Book(BaseMedia):
    author = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(5, message="Author must be at least 5 characters long")
        ]
    )
    isbn = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            MinLengthValidator(6, message="ISBN must be at least 6 characters long")
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Book"
        verbose_name_plural = "Models of type - Book"

class Movie(BaseMedia):
    director = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(8, message="Director must be at least 8 characters long")
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Movie"
        verbose_name_plural = "Models of type - Movie"

class Music(BaseMedia):
    artist = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(9, message="Artist must be at least 9 characters long")
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Music"
        verbose_name_plural = "Models of type - Music"




class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_tax(self) -> Decimal:
        return self.price * 0.08

    @staticmethod
    def calculate_shipping_cost(weight: Decimal) -> Decimal:
        return weight * 2

    def format_product_name(self) -> str:
        return f"Product: {self.name}"

class DiscountedProduct(Product):
    def calculate_price_without_discount(self) -> Decimal:
        return self.price * 1.20

    def calculate_tax(self) -> Decimal:
        return self.price * 0.05

    @staticmethod
    def calculate_shipping_cost(weight: Decimal) -> Decimal:
        return weight * 1.50

    def format_product_name(self):
        return f"Discounted Product: {self.name}"

    class Meta:
        proxy = True





class RechargeEnergyMixin:
    MAX_ENERGY: int = 100

    def recharge_energy(self, amount: int) -> None:
        self.energy = min(self.MAX_ENERGY, self.energy + amount)


class Hero(models.Model, RechargeEnergyMixin):
    name = models.CharField(max_length=100)
    hero_title = models.CharField(max_length=100)
    energy = models.PositiveIntegerField()

    @property
    def energy_usage_units(self):
        pass

    @property
    def unsuccessful_energy_usage_units_message(self):
        pass

    @property
    def successful_message(self):
        pass

    def energy_usage(self) -> str:
        if self.energy < self.energy_usage_units:
            return self.unsuccessful_energy_usage_units_message

        self.energy = max(self.energy - self.energy_usage_units, 1)
        self.save()
        return self.successful_message


class SpiderHero(Hero):
    @property
    def energy_usage_units(self):
        return 80

    @property
    def unsuccessful_energy_usage_units_message(self):
        return f"{self.name} as Spider Hero is out of web shooter fluid"

    @property
    def successful_message(self):
        return f"{self.name} as Spider Hero swings from buildings using web shooters"

    def swing_from_buildings(self):
        return self.energy_usage()

    class Meta:
        proxy = True


class FlashHero(Hero):
    @property
    def energy_usage_units(self):
        return 65

    @property
    def unsuccessful_energy_usage_units_message(self):
        return f"{self.name} as Flash Hero needs to recharge the speed force"

    @property
    def successful_message(self):
        return f"{self.name} as Flash Hero runs at lightning speed, saving the day"

    def run_at_super_speed(self):
        return self.energy_usage()

    class Meta:
        proxy = True

