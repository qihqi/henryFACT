from django.core.management import setup_environ
from django.db import transaction
import sys
sys.path.append('/var/servidor/henry')
import settings
setup_environ(settings)

from facturas.models import *
from productos.models import *
from decimal import Decimal
import datetime
import traceback
import json


def dump_row(row):
    return json.dumps({
        'producto': row.producto_id,
        'cantidad': int(row.cantidad * 1000),
        'tipo': row.ingreso_cod.tipo,
        'fecha': row.ingreso_cod.fecha.isoformat(),
        'bodega': row.ingreso_cod.bodega_id,
        'bodega_desde': row.ingreso_cod.bodega_desde_id,
        })


def main():
    all_rows = IngresoItem.objects.filter(ingreso_cod__fecha__gte=datetime.datetime(2013,11,11))
    for row in all_rows:
        print dump_row(row)

main()
