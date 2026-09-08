import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Product, Order
from django.db.models import Q, F
from django.db.models.aggregates import Count
from decimal import Decimal

# Create queries within functions
def populate_db():
    profile1 = Profile.objects.create(
        full_name='Profile 1',
        email='profile1@abv.bg',
        phone_number='+359883733073',
        address='Address 1'
    )
    profile2 = Profile.objects.create(
        full_name='Profile 2',
        email='profile2@abv.bg',
        phone_number='+359883737073',
        address='Address 2'
    )

    product1 = Product.objects.create(
        name='Product 1',
        description='Description 1',
        price=23.98,
        in_stock=5,
    )
    product2 = Product.objects.create(
        name='Product 2',
        description='Description 2',
        price=24.98,
        in_stock=3,
    )

    order1 = Order.objects.create(
        profile=profile1,
        total_price=35.99,
    )
    order2 = Order.objects.create(
        profile=profile2,
        total_price=45.97,
    )

    order1.products.add(product1)
    order2.products.add(product2, product1)



def get_profiles(search_string=None) -> str:
    if search_string is None:
        return ''

    profiles = Profile.objects.filter(
        Q(full_name__icontains=search_string) |
        Q(email__icontains=search_string) |
        Q(phone_number__icontains=search_string)
    ).order_by('full_name')

    if not profiles:
        return ''

    return '\n'.join(
        f"Profile: {p.full_name}, "
        f"email: {p.email}, "
        f"phone number: {p.phone_number}, "
        f"orders: {p.orders.count()}"
        for p in profiles
    )

def get_loyal_profiles() -> str:
    profiles = Profile.objects.get_regular_customers()

    if not profiles:
        return ''

    return '\n'.join(
        f"Profile: {p.full_name}, orders: {p.orders.count()}"
        for p in profiles
    )

def get_last_sold_products() -> str:
    latest_order = (Order.objects.prefetch_related('products')
                    .order_by('creation_date').last())

    if not latest_order or latest_order.products.count() == 0:
        return ''

    last_sold_products = ', '.join(
        p.name for p in latest_order.products.order_by('name')
    )

    return f"Last sold products: {last_sold_products}"





def get_top_products() -> str:
    top_products = Product.objects.get_products_by_orders_count()

    if not top_products or top_products[0].number_of_orders == 0:
        return ''

    if top_products.count() > 5:
        top_products = top_products[:5]

    return '\n'.join(
        f"{p.name}, sold {p.number_of_orders} times"
        for p in top_products
    )

def apply_discounts() -> str:
    updated_orders = Order.objects.annotate(
        number_of_products=Count('products'),
    ).filter(
        number_of_products__gt=2,
        is_completed=False,
    ).update(
        total_price=F('total_price') * Decimal("0.90"),
    )

    return f"Discount applied to {updated_orders} orders."

def complete_order() -> str:
    order = Order.objects.filter(
        is_completed=False,
    ).order_by('creation_date').first()

    if not order:
        return ''

    order.is_completed = True
    order.save()

    products_to_be_updated = []
    for p in order.products.all():
        if p.in_stock > 0:
            p.in_stock -= 1

            if p.in_stock == 0:
                p.is_available = False

        products_to_be_updated.append(p)

    Product.objects.bulk_update(products_to_be_updated, ['in_stock', 'is_available'])
    return "Order has been completed!"

