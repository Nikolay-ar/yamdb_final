import re

from django.core.exceptions import ValidationError

PATTERN = r'[^\w.@+-]+'
SYMBOL_NAMES = {' ': 'пробел', ',': 'запятая', '/': 'слэш', '\\': 'бэк-слэш'}


def symbol_name(symbol):
    return SYMBOL_NAMES.get(symbol, symbol)


def username_validator(value):
    if value == 'me':
        raise ValidationError(
            'Для имени пользователя нельзя использовать «me»'
        )
    incorrect = list(set(''.join(re.findall(PATTERN, value))))
    if incorrect:
        raise ValidationError(
            (f'Символы {", ".join(map(symbol_name, incorrect))} '
             'нельзя использовать в имени')
        )
    return value
