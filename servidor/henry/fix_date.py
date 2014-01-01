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


def fix_dates(inv):
    ordenes = list(OrdenDeDespacho.objects.filter(
            codigo=inv['codigo'],
            bodega_id=inv['bodega']))
    if ordenes:
        orden = ordenes[0]
        orden.fecha = inv['fecha']
        orden.save()
        print 'orden', orden.codigo, ' a fecha', orden.fecha
    else:
        print >>sys.stderr, 'orden no encontrado', inv['codigo'], inv['bodega']


def main():
    with open(sys.argv[1]) as f:
        i = 0
        for line in f.readlines():
            fix_dates(json.loads(line))


if __name__ == '__main__':
    main()

