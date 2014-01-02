from django.core.management import setup_environ
from django.db import transaction
import sys
sys.path.append('/var/servidor/henry')
import settings
setup_environ(settings)

from facturas.models import *
from productos.models import *
from productos.controllers import *
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



CONVERT_CODE = {
        "BPAT": "ACPCO" ,
        "BGUN": "BOTG",
        "GX3PTL": "GIRX3P" ,
        "TENPE":"TENPEQ",
        "VINCHAS4": "VINCHAS 4",
        "VINCHAS5": "VINCHAS 5"}


def inc(row):
    masProd(Bodega(id=row['bodega']), row['cantidad'], row['producto'])

def dec(row):
    menosProd(Bodega(id=row['bodega']), row['cantidad'], row['producto'])

def trans(row):
    masProd(Bodega(id=row['bodega']), row['cantidad'], row['producto'])
    menosProd(Bodega(id=row['bodega_desde']), row['cantidad'], row['producto'])

def imp(row):
    with open('reempaque', 'a') as f:
        print >>f, json.dumps(row)

trans_type = {
        Ingreso.TIPO_INGRESO: inc,
        Ingreso.TIPO_EXTERNA: dec,
        Ingreso.TIPO_TRANSFERENCIA: trans,
        Ingreso.TIPO_REEMPAQUE: imp
    }
def insert_trans(row):
    cod = row['producto']
    if cod in CONVERT_CODE:
        cod = CONVERT_CODE[cod]
        row['producto'] = cod
    if row['tipo'] != Ingreso.TIPO_REEMPAQUE:
        row['cantidad'] = Decimal(row['cantidad']) / 1000
    func = trans_type[row['tipo']]
    func(row)


def main():
    with open(sys.argv[1]) as f:
        i = 1
        for x in f.readlines():
            row = json.loads(x.strip())
            insert_trans(row)
            print >>sys.stderr, i,
            try:
                print row['producto'], 'hecho'
            except Exception:
                print
                pass
            i += 1

main()
