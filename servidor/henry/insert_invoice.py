from django.core.management import setup_environ
from diango.db import transaction
import sys
sys.path.append('/var/servidor/henry')
import settings
setup_environ(settings)

from facturas.models import *
from decimal import Decimal
import datetime


def _cent_to_decimal(cent):
    return Decimal(cent) / 100


def insert_invoice(inv):
    items = inv['items']
    orden = OrdenDeDespacho(
            codigo=inv['codigo'],
            bodega_id=inv['bodega'],
            cliente_id=inv['cliente'],
            fecha=datetime.datetime.strptime(inv['fecha'], "%Y-%m-%d")
            total=_cent_to_decimal(inv['total'],
            desc=_cent_to_decimal(inv['desc']) if inv['desc'] else None,
            pago=inv['pago'],
            precio_modificado=inv['precio_modificado'],
            eliminado=inv['eliminado'])
    orden.save()

    for i in items:
        item = ItemDeDespacho(
                desp_cod_id=i['producto'],
                precio=_cent_to_decimal(i['precio']),
                cantidad=Decimal(i['cantidad']) / 1000,
                precio_modificado=i['precio_modificado'])
        cant = Contenido.objects.filter(prod_id=item.desp_cod_id, bodega_id=orden.bodega_id)[0]
        cant.cantidad -= item.cantidad
        cant.save()
        item.save()


def main():
    with open(sys.argv[1]) as f:
        for line in f.readlines():
            try:
                obj = json.loads(line.strip())
                insert_invoice(obj)
            except Exception as e:
                print line
                break

