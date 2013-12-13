from productos.models import *
from facturas.models import *
from datetime import date, timedelta
import operator
def most_selled_quantity(n, bodega):
    return get_most_selled(n, bodega, lambda x : x.cantidad)
def most_selled_value(n, bodega):
    return get_most_selled(n, bodega, lambda x : x.precio * x.cantidad)

def get_most_selled(n, bodega, func):
    facturas = OrdenDeDespacho.objects \
               .filter(fecha__range=(date.today() - timedelta(days=7), date.today())) \
               .filter(bodega_id=bodega)
    prod = {}
    for f in facturas:
        for item in f.itemdedespacho_set.all():
            delta = func(item)
            if item.producto_id not in prod:
                prod[item.producto_id] = delta
            else:
                prod[item.producto_id] += delta

    result = sorted(prod.iteritems(), key=operator.itemgetter(1), reverse=True)

    return result[:n]


