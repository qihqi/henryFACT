from django import template

register = template.Library()

@register.filter
def absolute(val):
    return abs(val)
