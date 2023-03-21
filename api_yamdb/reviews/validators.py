import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(data):
    if data > dt.datetime.now().year:
        raise ValidationError(
            'Нельзя добавлять произведения, которые еще не вышли ')
    return data
