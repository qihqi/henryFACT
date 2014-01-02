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


def fix_dates(line):
    inv = json.loads(line)
    ordenes = list(OrdenDeDespacho.objects.filter(
            codigo=inv['codigo'],
            bodega_id=inv['bodega']))
    if ordenes:
        orden = ordenes[0]
        print >>sys.stderr, 'orden', orden.codigo, ' a fecha', orden.fecha
    else:
        print line.strip()


def main():
    with open(sys.argv[1]) as f:
        for line in f.readlines():
            fix_dates(line)


if __name__ == '__main__':
    main()

