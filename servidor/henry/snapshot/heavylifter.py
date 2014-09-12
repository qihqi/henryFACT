#aqui hace los trabajo realmente
from snapshot.models import *
from productos.models import *
from facturas.models import *
from django.db.models import Max
from datetime import date
from django.db.models import Q

import random
import itertools
def parse_date(st):
    return date(*map(int, st.split('-')))

def get_last_fecha():
    last_fecha = Snapshot.objects.aggregate(Max('fecha'))['fecha__max']

def get_top_records(number, fecha, column):
    query = Snapshot.objects
    if fecha:
        query = query.filter(fecha__lte=fecha)

    last_fecha =query.aggregate(Max('fecha'))['fecha__max']
    result = []
    for (bod, tipo) in itertools.product((1,2), (1,2)):
        objs = Snapshot.objects.filter(bodega_id=bod,
                                   prod__categoria_id=tipo,
                                   fecha=last_fecha).order_by(column)[:number]
        result.append(objs)
    return result


def get_revision(bodega, tipo):
    return get_full_random_revision(bodega, tipo)
    last_fecha = Snapshot.objects.aggregate(Max('fecha'))['fecha__max']

    objs = Snapshot.objects.filter(bodega_id=bodega,
                                   prod__categoria_id=tipo,
                                   fecha=last_fecha).order_by("-venta_cant")
    objs_zero = objs.filter(venta_cant=0)

    size = objs.count()
    size_zero = objs_zero.count()

    index1 = 0
    index2 = 0
    if size - size_zero > 10:
        index1 = random.randint(0, 10)
        index2 = random.randint(11, size - size_zero - 1)
    else:
        index1 = random.randint(0, size - 1)
        index2 = random.randint(0, size - 1)
    index3 = random.randint(0, size_zero-1)

    if size_zero == 0:
        index2 = random.randint(11, size -  11)
        index3 = random.randint(size - 10, size - 1)

    obj1 = objs[index1]
    obj2 = objs[index2]
    obj3 = objs[index3] if size_zero==0 else objs_zero[index3]

    return (obj1.contenido, obj2.contenido, obj3.contenido)


def get_full_random_revision(bodega, tipo):
    a_ind = ord('A')
    z_ind = ord('Z')

    candidates = set()
    while len(candidates) < 3:
        r = random.randint(a_ind, z_ind + 1)
        candidates.add(chr(r))

    c= tuple(candidates)
    thefilter = Q(prod__codigo__startswith=c[0]) | Q(prod__codigo__startswith=c[1]) | Q(prod__codigo__startswith=c[2])
    print thefilter
    choosen = Contenido.objects.filter(thefilter)
    size = choosen.count()
    contenidos = set()
    while len(contenidos) < 3:
        contenidos.add(random.randint(0, size-1))

    return [choosen[i] for i in contenidos]




#------------------------------------------------------------------------------------
def update_record():
    contenidos = Contenido.objects.all()

    for cont in contenidos:
        if get_last_record(cont) == date.today():
            continue
        venta_cant, venta_valor = get_vendidos(cont)
        ingreso_cant = get_ingresados(cont)
        snap = Snapshot( fecha=date.today(),
                         bodega_id=cont.bodega_id,
                         prod_id=cont.prod_id,
                         cant=cont.cant,
                         precio=cont.precio,
                         precio2=cont.precio2,
                         venta_cant=venta_cant,
                         venta_valor=venta_valor,
                         ingreso_cant=ingreso_cant,
                         )
        snap.save()

def get_last_record(cont):
    all_snap = Snapshot.objects.filter(bodega_id=cont.bodega_id,
                                    prod_id=cont.prod_id)
    if all_snap.count() > 0:
        return all_snap.aggregate(Max('fecha'))['fecha__max']

def get_vendidos(cont):
    desde = get_last_record(cont)
    hasta = date.today()

    items = ItemDeDespacho.objects.filter(
                desp_cod__bodega_id=cont.bodega_id,
                producto_id=cont.prod_id,
                desp_cod__eliminado=False
            )

    if desde:
        items = items.filter(desp_cod__fecha__range=(desde, hasta))
    else:
        items = items.filter(desp_cod__fecha__lte=hasta)

    venta_cant = 0
    venta_valor = 0
    for i in items:
        venta_cant += i.cantidad
        venta_valor += i.precio * i.cantidad

    return venta_cant, venta_valor

def get_ingresados(cont):
    desde = get_last_record(cont)
    hasta = date.today()

    items = IngresoItem.objects.filter(producto_id=cont.prod_id)
    if desde:
        items = items.filter(ingreso_cod__fecha__range=(desde, hasta))
    else:
        items = items.filter(ingreso_cod__fecha__lte=hasta)

    def get_ext_sign(ingreso):
        try:
            detalle = ingreso.ingresodetalle
            if not detalle.posteado:
                return 0
            return 1 if detalle.entrada else -1
        except Exception:
            return 0

    def get_reemp_sign(ingreso):
        if ingreso.bodega_id != cont.bodega_id:
            return 0
        try:
            x = ingreso.ingresodetalle.ingreso_id
            return -1
        except IngresoDetalle.DoesNotExist:
            return 1

    sign = {Ingreso.TIPO_INGRESO: (lambda b : 1 if b.bodega_id==cont.bodega_id else 0),
            Ingreso.TIPO_TRANSFERENCIA: (lambda b : -1 if b.bodega_id==cont.bodega_id else 1),
            Ingreso.TIPO_EXTERNA: get_ext_sign,
            Ingreso.TIPO_REEMPAQUE: get_reemp_sign,
            }

    delta = 0
    for i in items:
        delta += sign[i.ingreso_cod.tipo](i.ingreso_cod) * i.cantidad

    return delta
