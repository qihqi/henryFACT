from productos.models import *
from decimal import Decimal

#header = dict containing infos to create ingreso
#items = iterable of (cantidad, producto) pair
#call back = function that further modify state, takes (cant, producto) pair
#default callback does nothing
def makeIngreso(header, items, callback = lambda c,p : None):
    ing = Ingreso(**header)
    ing.save()
    bodega = ing.bodega
    for counter, item in enumerate(items):
        ing.ingresoitem_set.create(
                        num=counter,
                        cantidad=Decimal(item[0]),
                        producto_id=item[1])
        callback(item[0], item[1])
    return ing

def positive(num):
    return num if num > 0 else 0

def menosProd(bodega, delta, codigo):
    modificarCantidad(bodega,  -positive(delta), codigo)

def masProd(bodega,  delta, codigo):
    modificarCantidad(bodega,positive(delta), codigo)

def modificarCantidad(bodega,  delta, codigo):
    try:
        print 'called', bodega.id, delta, codigo
    except Exception:
        pass
    cont = Contenido.objects.get(bodega=bodega, prod_id=codigo)
    cont.cant += delta
    cont.save()
