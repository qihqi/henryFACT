from django.core.management import setup_environ
import sys
sys.path.append('/var/servidor/henry')
import settings
setup_environ(settings)

from facturas.models import *

all_despacho = OrdenDeDespacho.objects.all()
for desp in all_despacho:
    desp_dict = {
        'codigo': desp.codigo,
        'bodega': desp.bodega,
        'vendedor': desp.vendedor,
        'cliente':desp.cliente,
        'fecha':desp.fecha,
        'total':desp.total,
        'desc':desp.desc,
        'pago':desp.pago,
        'precio_modificado': desc.precio_modificado
        'items' : []
    }
    for item in ItemDeDespacho.objects.filter(desp_cod_id=desp.id):
        desp_dict['items'].append({
            'producto',
            'precio',
            'cantidad',
            'precio_modificado'
        })
