from django import template

register = template.Library()

@register.filter
def multi(value):
    return value * -1
