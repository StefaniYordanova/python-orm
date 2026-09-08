from django.core.exceptions import ValidationError


def validate_customer_name(value):
    if any(not l.isalpha() or l != ' ' for l in value):
        raise ValidationError("Name can only contain letters and spaces")

def validate_customer_phone_number(value):
    if not(value.startswith("+359") and len(value[4:]) == 9):
        raise ValidationError("Phone number must start with '+359' followed by 9 digits")

