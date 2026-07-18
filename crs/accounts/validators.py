import phonenumbers
from django.core.exceptions import ValidationError


def validate_phone(value):
    try:
        phone = phonenumbers.parse(value, None)
    except phonenumbers.NumberParseException:
        raise ValidationError("Введите корректный номер телефона.")

    if not phonenumbers.is_valid_number(phone):
        raise ValidationError("Введите корректный номер телефона.")