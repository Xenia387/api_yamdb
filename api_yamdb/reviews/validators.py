from datetime import datetime
from django.core.exceptions import ValidationError


def validate_year(value):
    current_year = datetime.now().year
    if value < 1920 or value > current_year:
        raise ValidationError(
            f"Значение года должно быть целым числом от 1920 до {current_year}",
            params={"value": value},
        )