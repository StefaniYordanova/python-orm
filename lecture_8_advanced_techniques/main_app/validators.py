from django.core.exceptions import ValidationError


def validate_menu_categories(value):
    categories = ["Appetizers", "Main Course", "Desserts"]
    if not all(c.lower() in value.lower() for c in categories):
        raise ValidationError('The menu must include each of the '
                              'categories "Appetizers", "Main Course", '
                              '"Desserts".')