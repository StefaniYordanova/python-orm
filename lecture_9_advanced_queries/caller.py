import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Product, Category, Customer, Order, OrderProduct
from django.db.models import Sum, F

# Create and run queries
def product_quantity_ordered() -> str:
    orders = Product.objects.annotate(
        total=Sum("orderproduct__quantity")
    ).exclude(total=None).values('name', 'total').order_by("-total")

    return '\n'.join(f"Quantity ordered of {o['name']}: {o['total']}"
                     for o in orders)

def ordered_products_per_customer() -> str:
    orders = Order.objects.prefetch_related("orderproduct_set__product__category").order_by('id')

    result = []
    for o in orders:
        result.append(f"Order ID: {o.id}, Customer: {o.customer.username}")

        for p in o.orderproduct_set.all():
            result.append(f"- Product: {p.product.name}, Category: {p.product.category.name}")

    return '\n'.join(result)

def filter_products() -> str:
    products = Product.objects.filter(is_available=True, price__gt=3).order_by("-price", "name")
    return '\n'.join(f"{p.name}: {p.price}lv." for p in products)

def give_discount() -> str:
    (Product.objects.filter(is_available=True, price__gt=3)
     .update(price=F('price') * 0.7))

    return '\n'.join(f"{p.name}: {p.price}lv." for p in Product.objects.filter(is_available=True).order_by('-price', 'name'))

