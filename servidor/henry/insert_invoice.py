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

CONVERT_CODE = {
        "BPAT": "ACPCO" ,
        "BGUN": "BOTG",
        "GX3PTL": "GIRX3P" ,
        "TENPE":"TENPEQ",
        "VINCHAS4": "VINCHAS 4",
        "VINCHAS5": "VINCHAS 5"}

def _cent_to_decimal(cent):
    return Decimal(cent) / 100

def fix_codigo(i):
    if i['producto'] in CONVERT_CODE:
        i['producto'] = CONVERT_CODE[i['producto']]


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

    ordenes = list(OrdenDeDespacho.objects.filter(
            codigo=inv['codigo'],
            bodega_id=inv['bodega']))
    orden = None
    if ordenes:
        print >>sys.stderr, 'orden', inv['codigo'], 'existe, retorno'
        with open('ordenes_existentes', 'a') as f:
            print >>f, json.dumps(inv)
        return
        if ordenes[0].cliente_id == inv['cliente']:
            orden = ordenes[0]
        else:
            raise Exception('let it retry')
    else:
        orden = OrdenDeDespacho(
            codigo=inv['codigo'],
            bodega_id=inv['bodega'],
            vendedor_id=inv['vendedor'],
            cliente_id=inv['cliente'],
            fecha=datetime.datetime.strptime(inv['fecha'], "%Y-%m-%d"),
            total=_cent_to_decimal(inv['total']),
            desc=_cent_to_decimal(inv['desc']) if inv['desc'] else None,
            pago=inv['pago'],
            precio_modificado=inv['precio_modificado'],
            eliminado=inv['eliminado'])
        orden.save()

    x = 0
    for i in items:
        fix_codigo(i)
#        items = ItemDeDespacho.objects.filter(
#                desp_cod_id=orden.id,
#                producto_id=i['producto'])
#        if list(items):
#            print >>sys.stderr, items, 'already exists, passing'
#            x+=1
#            continue

        item = ItemDeDespacho(
                desp_cod_id=orden.id,
                precio=_cent_to_decimal(i['precio']),
                producto_id=i['producto'],
                cantidad=Decimal(i['cantidad']) / 1000,
                num=x,
                precio_modificado=i['precio_modificado'])

        try:
            if not orden.eliminado:
                cant = Contenido.objects.filter(prod_id=item.producto_id, bodega_id=orden.bodega_id)[0]
                cant.cant -= item.cantidad
                cant.save()
            item.save()
            x += 1
        except Exception as e:
            print >>sys.stderr, 'fatal:', item.producto_id, orden.bodega_id
            print >>sys.stderr, 'item', item
            raise


def main():
    count = 8258
    with open(sys.argv[1]) as f:
        i = 0
        for line in f.readlines():
            obj = json.loads(line.strip())
            try:
                insert_invoice(obj)
                print >>sys.stderr, i, 'success'
                i += 1
            except Exception as e:
                if obj['bodega'] == 2:
                    count += 1
                    obj['codigo'] = count
                    try:
                        insert_invoice(obj)
                        print >>sys.stderr, i, 'success'
                        i += 1
                    except Exception as e:
                        print line
                        raise
                else:
                    print line


if __name__ == '__main__':
    main()

