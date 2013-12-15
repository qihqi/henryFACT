from django import template
from decimal import Decimal
import decimal

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

@register.filter
def get_valor_neto(val):
    neto = val / Decimal('1.12')
    return '%.2f' % neto
        
@register.filter
def get_valor_neto_string(val):
    try:
        neto = Decimal(val) / Decimal('1.12')
        return '%.2f' % neto
    except decimal.InvalidOperation:
        return ''
