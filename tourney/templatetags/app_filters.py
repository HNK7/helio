from django import template

register = template.Library()


@register.filter(name='format_phone_number')
def format_phone_number(number):
    return '(%s%s%s) %s%s%s-%s%s%s%s' % tuple(number)


@register.filter(name="format_card_number")
def format_card_number(number):
    return '%s%s%s%s %s%s%s%s %s%s%s%s %s%s%s%s' % tuple(number)
