from snapshot.heavylifter import *
from django.shortcuts import render_to_response, redirect
from datetime import date
from main.views import my_login_required
from django.core.urlresolvers import reverse
from datetime import date, timedelta
@my_login_required
def revisar_inventario(request):
    flores_alm = get_revision(bodega=1, tipo=1)
    bisu_alm = get_revision(bodega=1, tipo=2)
    flores_bod = get_revision(bodega=2, tipo=1)
    bisu_bod = get_revision(bodega=2, tipo=2)
    return render_to_response('revision.html',
                             {'flores_alm' : flores_alm,
                                'bisu_alm' : bisu_alm,
                                'flores_bod' : flores_bod,
                                'bisu_bod': bisu_bod,
                                'fecha' : date.today().isoformat()
                                })

@my_login_required
def revisar_estado_cant(request):
    number = request.GET.get('number', 20)
    if not number:
        number = 20
    fecha = request.GET.get('fecha', None)
    if not fecha:
        fecha = None
    rec_cant = get_top_records(number, fecha, '-venta_cant')
    return render_to_response('display_record.html',
                             {'flores_alm' : rec_cant[0],
                              'bisu_alm' : rec_cant[1],
                              'flores_bod' : rec_cant[2],
                              'bisu_bod' : rec_cant[3],
                              'action' : reverse('snapshot.views.revisar_estado_cant'),
                             })

@my_login_required
def revisar_estado_value(request):
    number = request.GET.get('number', 20)
    if not number:
        number = 20
    fecha = request.GET.get('fecha', None)
    if not fecha:
        fecha = None
    rec_cant = get_top_records(number, fecha, '-venta_valor')
    return render_to_response('display_record.html',
                             {'flores_alm' : rec_cant[0],
                              'bisu_alm' : rec_cant[1],
                              'flores_bod' : rec_cant[2],
                              'bisu_bod' : rec_cant[3],
                              'action' : reverse('snapshot.views.revisar_estado_value'),
                             })

@my_login_required
def ver_prod_hist(request, codigo, bodega):
    desde = request.GET.get('desde', None)
    hasta = request.GET.get('hasta', None)

    if desde:
        tmp = desde.split('-')
        desde = date(int(tmp[0]), int(tmp[1]), int(tmp[2]))
    else:
        desde = date.today() - timedelta(days=77)

    if hasta:
        tmp = hasta.split('-')
        hasta = date(int(tmp[0]), int(tmp[1]), int(tmp[2]))
    else:
        hasta = date.today()

    tables = Snapshot.objects.filter(fecha__range=(desde, hasta),
                                     prod_id=codigo,
                                     bodega_id=bodega).order_by('fecha')

    prod = Producto.objects.get(codigo=codigo)
    bod = Bodega.objects.get(id=bodega)

    return render_to_response('prod_detalle.html',
                             {'items' : tables,
                              'prod': prod,
                              'bodega' : bod,
                              'desde' : desde.isoformat(),
                              'hasta' : hasta.isoformat(),
                             })






