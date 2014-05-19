import functools
from decimal import Decimal

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import user_passes_test

from facturas.forms import *
from main.views import my_login_required
from main.helper import render_form
from main.models import *
from facturas.models import *
from productos.models import *
from productos.views import generar_ingreso_page
from productos.reempaque import ver_reempaque


#Resumen de venta, la ventana de busqueda
@my_login_required
@user_passes_test(hasNivel(1), '/r/login')
def resumen_request_page(request):
    #make an empty form
    form = ResumenForm(initial={'desde': date.today(), 'hasta': date.today()})
    meta = {'method': 'get',
            'form': form,
            'st_message': '',
            'action': reverse('facturas.views.generar_resumen_page'),
            'submit_name': 'Buscar',
            'title': 'Resumen de Venta',
    }

    return render_form(meta, RequestContext(request))


def resumen_menorista(desde, hasta, vendido, condensado=False):
    resumen = OrdenDeDespacho.objects.filter(fecha__range=(desde, hasta),
                                             vendedor=UserJava(username=vendido),
                                             bodega=Bodega(1))
    validos = resumen.filter(eliminado=False)

    if condensado:
        validos = resumen_condensado(validos).values()
        return render_to_response('resumen_condensado.html', {
            'bodega': 'ALMACEN',
            'desde': desde,
            'hasta': hasta,
            'validos': validos
        })

    borrados = list(resumen.filter(eliminado=True))

    cf = list(validos.filter(cliente_id='NA'))
    otros = list(validos.exclude(cliente_id='NA'))

    ftotal = lambda n, f: n + f.total
    ctotal = reduce(ftotal, cf, 0)
    ototal = reduce(ftotal, otros, 0)
    btotal = reduce(ftotal, borrados, 0)

    tot = len(cf)

    lista = []
    for i in range(0, tot, 3):
        end = i + 3 if i + 3 < tot else tot
        lista.append(cf[i:end])

    gran_total = ctotal + ototal
    total_neto_numero = gran_total / Decimal(1.12)
    total_neto = "%.2f" % total_neto_numero
    iva = "%.2f" % (gran_total - total_neto_numero)
    return render_to_response("resumen_menorista.html",
                              {'cf': lista,
                               'bodega': 'ALMACEN',
                               'desde': desde.isoformat(),
                               'hasta': hasta.isoformat(),
                               'vendedor': vendido,
                               'otros': otros,
                               'ctotal': ctotal,
                               'ototal': ototal,
                               'gtotal': gran_total,
                               'neto': total_neto,
                               'iva': iva,
                               'btotal': btotal,
                               'borrados': borrados
                              })


#parse the request and generate the resume de venta
@my_login_required
@user_passes_test(hasNivel(1), '/r/login')
def generar_resumen_page(request):
    #necesita privilegio para ver resumen
    form = ResumenForm(request.GET)

    if not form.is_valid():
        form = ResumenForm(initial={'desde': date.today(), 'hasta': date.today()})
        meta = {'method': 'get',
                'form': form,
                'st_message': 'Datos invalidos',
                'action': reverse('facturas.views.generar_resumen_page'),
                'submit_name': 'Buscar',
                'title': 'Resumen de Venta',
        }
        return render_form(meta, RequestContext(request))

    desde = form.cleaned_data['desde']
    hasta = form.cleaned_data['hasta']
    vendido = form.cleaned_data['vendido_por']
    bodega_id = int(form.cleaned_data['bodega'])
    bodega_name = Bodega.objects.get(id=bodega_id)
    resumen = OrdenDeDespacho.objects.filter(fecha__range=(desde, hasta),
                                             vendedor=UserJava(username=vendido),
                                             bodega=Bodega(bodega_id))
    #if nivel no alcanza, no deja:
    bod = Bodega.objects.get(id=bodega_id)
    if not hasNivel(bod.nivel + 1)(request.user):
        form = ResumenForm(initial={'desde': date.today(), 'hasta': date.today()})
        meta = {'method': 'get',
                'form': form,
                'st_message': 'Escoja otra bodega',
                'action': reverse('facturas.views.generar_resumen_page'),
                'submit_name': 'Buscar',
                'title': 'Resumen de Venta',
        }
        return render_form(meta, RequestContext(request))

    condensado = form.cleaned_data['condensado']
    if bodega_id == 1:
        return resumen_menorista(desde, hasta, vendido, condensado)

    validos = resumen.filter(eliminado=False)
    borrados = list(resumen.filter(eliminado=True))
    cheques = list(validos.filter(pago=OrdenDeDespacho.PAGO_CHEQUE))
    efectivos = list(validos.filter(pago=OrdenDeDespacho.PAGO_EFECTIVO))
    depositos = list(validos.filter(pago=OrdenDeDespacho.PAGO_DEPOSITO))
    creditos = list(validos.filter(pago=OrdenDeDespacho.PAGO_CREDITO))
    varios = list(validos.filter(pago=OrdenDeDespacho.PAGO_VARIOS))

    cheque_total = sum([c.total for c in cheques])
    efectivo_total = sum([c.total for c in efectivos])
    deposito_total = sum([c.total for c in depositos])
    btotal = sum([c.total for c in borrados])
    rtotal = sum([c.total for c in creditos])
    vtotal = sum([c.total for c in varios])

    gran_total = cheque_total + efectivo_total + deposito_total + rtotal + vtotal
    total_neto = "%.2f" % (gran_total / Decimal(1.12))
    return render_to_response('resumen.html',
                              {'cheques': cheques,
                               'bodega': bodega_name,
                               'desde': desde.isoformat(),
                               'hasta': hasta.isoformat(),
                               'vendedor': vendido,
                               'efectivos': efectivos,
                               'depositos': depositos,
                               'creditos': creditos,
                               'varios': varios,
                               'ctotal': cheque_total,
                               'etotal': efectivo_total,
                               'ttotal': deposito_total,
                               'borrados': borrados,
                               'btotal': btotal,
                               'rtotal': rtotal,
                               'vtotal': vtotal,
                               'gran_total': gran_total,
                               'total_neto': total_neto
                              })


@my_login_required
@user_passes_test(hasNivel(1), '/r/login')
def ver_resumen_total(request):
    form = ResumenForm(request.GET)
    print 'total resumen'
    if not form.is_valid():
        form = ResumenForm(initial={'desde': date.today(), 'hasta': date.today()})
        meta = {'method': 'get',
                'form': form,
                'st_message': 'Datos invalidos',
                'action': reverse('facturas.views.get_resumen_total'),
                'submit_name': 'Buscar',
                'title': 'Resumen de Venta',
        }
        return render_form(meta, RequestContext(request))

    desde = form.cleaned_data['desde']
    hasta = form.cleaned_data['hasta']
    bodega = form.cleaned_data['bodega']
    #get all the users
    users = UserJava.objects.all()
    totales = []
    for user in users:
        totales.append(get_totales(user, desde, hasta, bodega))

    print 'i am here'
    return render_to_response('totales.html', {'totales': totales})


def get_totales_form(request):
    form = ResumenForm(initial={'desde': date.today(), 'hasta': date.today()})
    meta = {'method': 'get',
            'form': form,
            'st_message': '',
            'action': reverse('facturas.views.ver_resumen_total'),
            'submit_name': 'Buscar',
            'title': 'Resumen de Venta',
    }
    return render_form(meta, RequestContext(request))


def get_totales(user, desde, hasta, bodega_id):
    resumen = OrdenDeDespacho.objects.filter(fecha__range=(desde, hasta),
                                             vendedor=user,
                                             bodega=Bodega(bodega_id))
    validos = resumen.filter(eliminado=False)

    totales = {}
    f = lambda x, y: x + y.total
    totales['btotal'] = reduce(f, resumen.filter(eliminado=True), 0)
    totales['ctotal'] = reduce(f, validos.filter(pago=OrdenDeDespacho.PAGO_CHEQUE), 0)
    totales['etotal'] = reduce(f, validos.filter(pago=OrdenDeDespacho.PAGO_EFECTIVO), 0)
    totales['dtotal'] = reduce(f, validos.filter(pago=OrdenDeDespacho.PAGO_DEPOSITO), 0)
    totales['rtotal'] = reduce(f, validos.filter(pago=OrdenDeDespacho.PAGO_CREDITO), 0)

    totales['user'] = user.username
    return totales

# form para ver factura
@my_login_required
def ventas_por_productos(request):
    meta = {'method': 'get',
            'form': VerVentaPorProducto(),
            'st_message': '',
            'action': reverse('facturas.views.ventas_por_productos_detalle'),
            'submit_name': 'Ver',
            'title': 'Ver Ventas por Productos',
    }
    return render_form(meta, None)


# form para ver factura
@my_login_required
def ventas_por_productos_detalle(request):
    meta = {'method': 'get',
            'form': VerVentaPorProducto(),
            'st_message': '',
            'action': reverse('facturas.views.ventas_por_productos_detalle'),
            'submit_name': 'Ver',
            'title': 'Ver Ventas por Productos',
    }
    form = VerVentaPorProducto(request.GET)
    if not form.is_valid():
        meta['form'] = form
        return render_form(meta, None)


    desde = form.cleaned_data['desde']
    hasta = form.cleaned_data['hasta']
    codigo = form.cleaned_data['codigo']
    bodega_id = int(form.cleaned_data['bodega'])

    if not len(Producto.objects.filter(codigo=codigo)):
        meta['st_message'] = 'Producto %s no existe' % codigo
        return render_form(meta, None)

    all_venta_row = ItemDeDespacho.objects.filter(
            producto_id=codigo,
            desp_cod__fecha__gte=desde,
            desp_cod__fecha__lte=hasta,
            desp_cod__bodega_id=bodega_id)

    total = sum((i.cantidad for i in all_venta_row))

    return render_to_response('ventas_por_productos_detalle.html', {
        'total': total,
        'items': all_venta_row,
        'form': form,
        'prod': Producto.objects.get(codigo=codigo),
        'request': {
            'desde': desde,
            'hasta': hasta,
            'bodega': bodega_id
            }
        })



@my_login_required
#esto es para eliminar factura!
def testPage(request):
    meta = {'method': 'post',
            'form': None,
            'st_message': '',
            'action': reverse('facturas.views.testPage'),
            'submit_name': 'Eliminar',
            'title': 'Eliminar Factura',
    }
    if request.method == 'GET':
        meta['form'] = EliminarForm()
        return render_form(meta, RequestContext(request))

    form = EliminarForm(request.POST)
    if not form.is_valid():
        meta['form'] = form
        return render_form(meta, RequestContext(request))

    try:
        user = request.user
        codigo = form.cleaned_data['no_de_factura']
        motivo = form.cleaned_data['motivo']

        #hacer un record
        desp = OrdenDeDespacho.objects.get(codigo=codigo)
        if desp.eliminado:
            raise OrdenDeDespacho.DoesNotExist()

        bodega = desp.bodega
        record = OrdenEliminado(codigo=desp,
                                motivo=motivo,
                                eliminado_por=user)

        #devolver marcaderia
        items = ItemDeDespacho.objects.filter(desp_cod=desp)
        for item in items:
            cont = Contenido.objects.get(prod=item.producto, bodega=bodega)
            cont.cant += item.cantidad
            cont.save()
            #insertar record
        record.save()
        #mark the factura
        desp.eliminado = True
        desp.save()

        meta['form'] = EliminarForm()
        meta['st_message'] = 'Factura <b> %s </b> eliminado con exito' % codigo
    except OrdenDeDespacho.DoesNotExist:
        meta['form'] = EliminarForm()
        meta['st_message'] = 'Factura <b> %s </b> no existe' % codigo

    return render_form(meta, RequestContext(request))


def ver_doc_page(request, msg=''):
    form = VerDocForm()
    meta = {'method': 'get',
            'form': form,
            'st_message': msg,
            'action': reverse('facturas.views.show_doc_page'),
            'submit_name': 'Ver',
            'title': 'Ver Documentos',
    }
    return render_form(meta, None)


def show_doc_page(request):
    form = VerDocForm(request.GET)

    if not form.is_valid():
        return ver_doc_page(request)

    bodega = Bodega(int(form.cleaned_data['bodega']))
    codigo = form.cleaned_data['codigo']
    tipo = form.cleaned_data['tipo']
    try:
        funcs = {'nota': functools.partial(ver_factura, nota=True),
                 'factura': functools.partial(ver_factura, nota=False),
                 'ingreso': lambda bodega, codigo: generar_ingreso_page(Ingreso.objects.get(id=codigo)),
                 'reempaque': lambda bodega, codigo: ver_reempaque(codigo),
        }
        page = funcs[tipo](bodega, codigo)
    except ObjectDoesNotExist:
        return ver_doc_page(request, 'Documento no encontrado')

    if not page:
        return ver_doc_page(request, 'Documento no existe');
    return page


class item:
    def __init__(self, cod, nombre, cant, precio):
        self.cod = cod
        self.nombre = nombre
        self.cant = cant
        self.precio = precio

    @property
    def subtotalx(self):
        return (self.cant * self.precio)

    @property
    def subtotal(self):
        return "%.2f" % self.subtotalx


def ver_factura(bodega, codigo, nota):
    factura = None
    items_factura = None

    if nota:
        factura = NotaDeVenta.objects.get(id=codigo)
        items_factura = ItemDeVenta.objects.filter(venta_cod=factura).order_by('num')
    else:
        factura = OrdenDeDespacho.objects.get(codigo=codigo, bodega=bodega)
        items_factura = ItemDeDespacho.objects.filter(desp_cod=factura).order_by('num')

    items = [item(i.producto.codigo, i.producto.nombre, i.cantidad, i.precio) \
             for i in items_factura]

    total = "%.2f" % functools.reduce(lambda ac, it: ac + it.subtotalx, items, 0)
    return render_to_response('ver_factura.html', {'factura': factura,
                                                   'items': items,
                                                   'total': total,
                                                   'is_nota': nota})


class CondensedItem(object):
    pass


def resumen_condensado(orden_list):
    condensed = {}
    for orden in orden_list:
        if orden.cliente_id in condensed:
            x = condensed[orden.cliente_id]
            x.total += orden.total
            x.total_orden += 1
            neto = (orden.total / Decimal('1.12'))
            x.neto += neto
            iva = orden.total - neto
            x.total_iva += iva
        else:
            x = CondensedItem()
            x.total = orden.total
            x.total_orden = 1
            x.ruc = orden.cliente_id
            x.cliente = orden.cliente.fullname
            x.neto = orden.total / Decimal('1.12')
            x.total_iva = x.total - x.neto
            condensed[orden.cliente_id] = x

    for x in condensed.keys():
        condensed[x].total_iva = condensed[x].total_iva.quantize(Decimal('0.01'))
        condensed[x].neto = condensed[x].neto.quantize(Decimal('0.01'))

    return condensed




