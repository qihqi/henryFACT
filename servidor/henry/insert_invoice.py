from django.core.management import setup_environ
from django.db import transaction
import sys
sys.path.append('/var/servidor/henry')
import settings
setup_environ(settings)

from facturas.models import *
from decimal import Decimal
import datetime
import traceback
import json


def _cent_to_decimal(cent):
    return Decimal(cent) / 100


def fix_cliente(inv):
    cliente = Cliente.objects.filter(codigo=inv['cliente'])
    if list(cliente):
        return
    detalle = inv['cliente_detalle']
    detalle['cliente_desde'] = datetime.datetime.strptime(detalle['cliente_desde'], "%Y-%m-%d")
    cliente = Cliente(**detalle)
    cliente.save()     


def fix_producto(item):
    producto = Producto.objects.filter(codigo=item['producto'])
    if list(producto):
        return
    producto = list(Producto.objects.filter(nombre=item['producto_nombre']))
    if not producto:
        producto = list(Producto.objects.filter(nombre=item['producto_nombre'].strip()))
    if producto:
        with open('codigo_cambiado.txt', 'a') as f:
            print >>f, 'antes', item['producto'], 'despues', producto[0].codigo
        item['producto'] = producto[0].codigo
    else:
        with open('producto_nuevo.txt', 'a') as f:
            print >>f, item['producto']
         


def insert_invoice(inv):
    items = inv['items']
    fix_cliente(inv)
    orden = OrdenDeDespacho(
            codigo=inv['codigo'],
            vendedor_id=inv['vendedor'],
            bodega_id=inv['bodega'],
            cliente_id=inv['cliente'],
            fecha=datetime.datetime.strptime(inv['fecha'], "%Y-%m-%d"),
            total=_cent_to_decimal(inv['total']),
            desc=_cent_to_decimal(inv['desc']) if inv['desc'] else None,
            pago=inv['pago'],
            precio_modificado=inv['precio_modificado'],
            eliminado=inv['eliminado'])
    orden.save()

    num = 0
    for i in items:
        fix_producto(i)
        item = ItemDeDespacho(
                desp_cod_id=orden.id,
                num=num,
                precio=_cent_to_decimal(i['precio']),
                producto_id=i['producto'],
                cantidad=Decimal(i['cantidad']) / 1000,
                precio_modificado=i['precio_modificado'])

        try:
            cant = Contenido.objects.filter(prod_id=item.producto_id, bodega_id=orden.bodega_id)[0]
            cant.cant -= item.cantidad
            cant.save()
            item.save()
            num += 1
        except Exception as e:
            print >>sys.stderr, 'fatal:', item.producto_id, orden.bodega_id
            print >>sys.stderr, 'item', item
            raise


def main():
    with open(sys.argv[1]) as f:
        i = 0
        for line in f.readlines():
            try:
                obj = json.loads(line.strip())
                with transaction.atomic():
                    insert_invoice(obj)
                print >>sys.stderr, i, 'success'
                i += 1
            except Exception as e:
                print line
                raise

                


if __name__ == '__main__':
    main()

