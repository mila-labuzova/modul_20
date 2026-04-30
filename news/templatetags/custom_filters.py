from django import template
import re


register = template.Library()


CENSOR_WORDS = ['дурак', 'дурацкая', 'идиот', 'тупой']


@register.filter()
def censor(value):

    if not isinstance(value, str):
        raise TypeError('Фильтр "censor" применим только к строкам')

    result = value

    for c_word in CENSOR_WORDS:
        pattern = rf'\b({c_word[0].lower()}|{c_word[0].upper()}){c_word[1:]}\b'

        def replace(match):
            word = match.group(0)
            return word[0] + '*' * (len(word) - 1)

        result = re.sub(pattern, replace, result)

    return result