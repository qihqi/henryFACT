from django import template

register = template.Library()

@register.filter
def absolute(val):
    try:
        return abs(val)
    except TypeError:
        return ''
@register.filter
def get_range( value ):
    return range( value )
