from django.core.management import setup_environ
import sys
sys.path.append('/var/servidor/henry')
import settings
setup_environ(settings)

from facturas.models import *
import json
from datetime import datetime

def _as_centavo(s):
    return int(s * 100)

def dump_item(desp):
    desp_dict = {
        'codigo': desp.codigo,
        'bodega': desp.bodega_id,
        'vendedor': desp.vendedor_id,
        'cliente':desp.cliente_id,
        'fecha':desp.fecha.isoformat(),
        'total': _as_centavo(desp.total),
        'desc': _as_centavo(desp.desc) if desp.desc else None,
        'pago': desp.pago,
        'precio_modificado': desp.precio_modificado,
        'items' : []
    }
    for item in ItemDeDespacho.objects.filter(desp_cod_id=desp.id):
        desp_dict['items'].append({
            'producto': item.producto_id,
            'precio': _as_centavo(item.precio),
            'cantidad': int(item.cantidad * 1000),
            'precio_modificado': item.precio_modificado
        })
    return desp_dict


all_despacho = OrdenDeDespacho.objects.filter(fecha__gte=datetime(2013, 11,11))
for desp in all_despacho:
    print json.dumps(dump_item(desp))

