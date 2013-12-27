from django.core.management import setup_environ
import sys
sys.path.append('/var/servidor/henry')
import settings
setup_environ(settings)

from facturas.models import *

def _as_centavo(s):
    return int(s * 100)


all_despacho = OrdenDeDespacho.objects.all()
for desp in all_despacho:
    print json.dumps(dump_item(desp))

def dump_item(desp):
    desp_dict = {
        'codigo': desp.codigo,
        'bodega': desp.bodega,
        'vendedor': desp.vendedor,
        'cliente':desp.cliente,
        'fecha':desp.fecha.isoformat(),
        'total': _as_centavo(desp.total),
        'desc': _as_centavo(desp.desc),
        'pago':_as_centavo(desp.pago),
        'precio_modificado': desc.precio_modificado
        'items' : []
    }
    for item in ItemDeDespacho.objects.filter(desp_cod_id=desp.id):
        desp_dict['items'].append({
            'producto': item.producto,
            'precio': _as_centavo(item.precio),
            'cantidad': int(item.cantidad * 1000),
            'precio_modificado': item.precio_modificado
        })
    return desp_dict

