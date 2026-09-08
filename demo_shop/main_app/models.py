from django.db import models
from django.db.models import Q

# Create your models here.
class Customers(models.Model):

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(age__gte=18) & Q(age__lte=99),
                name="age_between_18_and_99",
            )
        ]

    class Gender(models.TextChoices):
        MALE = 'M'
        FEMALE = 'F'

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=Gender.choices)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    date_joined = models.DateField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Addresses(models.Model):
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=30)
    customer = models.OneToOneField('Customers', on_delete=models.CASCADE, related_name='address')

    def __str__(self):
        return self.city

class Orders(models.Model):

    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        SHIPPED = 'Shipped', 'Shipped'
        DELIVERED = 'Delivered', 'Delivered'

    order_date = models.DateField(auto_now_add=True, editable=False)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING)
    total_amount_products = models.PositiveIntegerField(default=1, verbose_name='Total amount of products')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey('Customers', on_delete=models.CASCADE, related_name='orders')

class Products(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey('Categories', on_delete=models.SET_NULL, null=True, related_name='products')
    order = models.ManyToManyField('Orders', related_name='products', through='OrderedItems')

    def __str__(self):
        return self.name

class Categories(models.Model):
    name = models.CharField(max_length=50)

class OrderedItems(models.Model):
    order = models.ForeignKey('Orders', on_delete=models.CASCADE)
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    product_quantity = models.PositiveIntegerField()
