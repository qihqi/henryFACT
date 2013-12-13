# Create your views here.
import traceback
import json
import functools
from decimal import Decimal
from datetime import date
from django.db import IntegrityError, transaction
from django.core.context_processors import csrf
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, UserManager
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt

from django.core import serializers

from main.helper import render_form
from main.views import my_login_required
from main.models import hasNivel
from productos.forms import *
from productos.models import *
from productos.controllers import *
from productos.api import *

@my_login_required
def create_bodega_page(request):
    form = CreateBodegaForm()
    meta = {'method' : 'post',
            'form' : form,
            'st_message' : '',
            'action' : reverse('productos.views.create_bodega_page'),
            'submit_name' : 'Crear',
            'title' : 'Crear Producto',
           }
    if request.method == 'GET':
        return render_form(meta, RequestContext(request))

    #handles post
    form = CreateBodegaForm(request.POST)
    if not form.is_valid():
        meta['form'] = form
        return render_form(meta, RequestContext(request))

    #Now the form is valid

    #enter transaction
    bodega = form.save()

    meta['st_message'] = 'Bodega <b> %s </b> es creado con exito' % bodega.nombre
    return render_form(meta, RequestContext(request))

@my_login_required
def create_cat_page(request):
    form = CreateCatForm()
    meta = {'method' : 'post',
            'form' : form,
            'st_message' : '',
            'action' : reverse('productos.views.create_cat_page'),
            'submit_name' : 'Crear',
            'title' : 'Crear Producto',
           }
    if request.method == 'GET':
        return render_form(meta, RequestContext(request))

    #handles post
    form = CreateCatForm(request.POST)
    if not form.is_valid():
        meta['form'] = form
        return render_form(meta, RequestContext(request))

    #Now the form is valid

    #enter transaction
    cat = form.save()

    meta['st_message'] = 'Categoria <b> %s </b> es creado con exito' % cat.nombre
    return render_form(meta, RequestContext(request))

@my_login_required
def create_product_page(request):
    form = CreateProductForm()
    meta = {'method' : 'post',
            'form' : form,
            'st_message' : '',
            'action' : reverse('productos.views.create_product_page'),
            'submit_name' : 'Crear',
            'title' : 'Crear Producto',
           }
    if request.method == 'GET':
        transaction.rollback()
        return render_form(meta, RequestContext(request))

    #handles post
    form = CreateProductForm(request.POST)
    if not form.is_valid():
        meta['form'] = form
        transaction.rollback()
        return render_form(meta, RequestContext(request))

    #Now the form is valid

    #enter transaction
    #Crear producto
    data = form.cleaned_data
    codigo = form.cleaned_data['codigo']
    nombre = form.cleaned_data['nombre']
    cat = int(form.cleaned_data['categoria'])
    prod = Producto(nombre=nombre, codigo=codigo, categoria=Categoria(cat))
    try:
        prod.save(force_insert=True)
    except IntegrityError:
        prod = Producto.objects.get(codigo=codigo)
        if nombre != '' and prod.nombre != nombre:
            meta['st_message'] = 'El codigo <b> %s </b> ya esta usado \
                                  para el producto <b> %s </b>; <br /> \
                                  Utilice otro codigo ' % (codigo, prod.nombre)
            transaction.rollback()
            return render_form(meta, RequestContext(request))


    #Crear transaction
    try:
        cont = Contenido(prod=prod,
                         precio=data['precio_menorista'],
                         precio2=data['precio_menorista_2'],
                         bodega_id=1,
                         cant=0)
        cont.save()
        cont = Contenido(prod=prod,
                         precio=data['precio_mayorista'],
                         precio2=data['precio_mayorista_2'],
                         bodega_id=2,
                         cant=0)
        cont.save()
    except IntegrityError:
        meta['st_message'] = 'Este producto ya existe en esta bodega'
        transaction.rollback()
        return render_form(meta, RequestContext(request))

    meta['st_message'] = 'Producto <b> %s </b> es creado con exito' % prod.nombre
    transaction.commit()
    return render_form(meta, RequestContext(request))

def validate_ingreso(post):
    try:
        codigos = post.getlist('codigo')
        cantidades = post.getlist('cant')
        bodega = post['bodega']
        #if len(codigos) != len(cantidades):
        #    raise Exception()
        for x in cantidades:
            if x != '':
                Decimal(x)
        int(bodega)
        return True
    except Exception as x:
        print x, type(x)
        return False

@my_login_required
def ingreso_producto_page(request):
    bodegas = Bodega.objects.all().exclude(id=-1)
    if request.method == 'GET':
        return render_to_response('ingreso.html',
                {'action' : reverse('productos.views.ingreso_producto_page'),
                 'bodegas' : bodegas,
                 'tipo' : 'I',
                },
                  context_instance=RequestContext(request))

    #insert the ingreso de bodega
    #transaction handled by middleware
    if not validate_ingreso(request.POST):
        return HttpResponse("Ingreso es falido")
    try:
        codigos = request.POST.getlist('codigo')
        cantidades = request.POST.getlist('cant')
        bodega = int(request.POST['bodega'])

        header = dict(usuario=request.user,
                          bodega_id=bodega,
                          tipo=Ingreso.TIPO_INGRESO)
        items = [(Decimal(c), p) for p, c in zip(codigos, cantidades) if p != '' and c != '']
        print items
        callback = functools.partial(masProd, Bodega(bodega))
        ingreso = makeIngreso(header, items, callback)
        transaction.commit()
        return generar_ingreso_page(ingreso)
    except Exception as x:
        transaction.rollback()
        print x,type(x)
        return HttpResponse('fallo el ingreso, intente de nuevo')

@my_login_required
def transfer_producto_page(request):
    transaction.commit()
    bodegas = Bodega.objects.all().exclude(id=-1)
    if request.method == 'GET':
        return render_to_response('ingreso.html',
                {'action' : reverse('productos.views.transfer_producto_page'),
                 'bodegas' : bodegas,
                 'tipo' : 'T',
                },
                  context_instance=RequestContext(request))
    try:
        codigos = request.POST.getlist('codigo')
        cantidades = request.POST.getlist('cant')
        bodega = int(request.POST['bodega'])
        desde = int(request.POST['desde'])

        header = dict(usuario=request.user,
                      bodega_id=bodega,
                      bodega_desde_id=desde,
                      tipo=Ingreso.TIPO_TRANSFERENCIA)

        items = [(Decimal(c), p) for p, c in zip(codigos, cantidades) if p != '' and c != '']

        def callback(cant, prod):
            masProd(Bodega(bodega), cant, prod)
            menosProd(Bodega(desde), cant, prod)

        ingreso = makeIngreso(header, items, callback)
        transaction.commit()
        return generar_ingreso_page(ingreso , True)

    except Exception as x:
        print x, type(x)
        transaction.rollback()
        return HttpResponse("fallo la transferencia")

@my_login_required
def ver_producto_page(request):
    meta = {'method' : 'get',
            'form' : VerProdForm(),
            'st_message' : '',
            'action' : reverse('productos.views.ver_page'),
            'submit_name' : 'Aceptar',
            'title' : 'Crear Producto',
           }

    return render_form(meta, RequestContext(request));

@my_login_required
def ver_page(request):
    form = VerProdForm(request.GET)
    if not form.is_valid():
        meta = {'method' : 'get',
                'form' : form,
                'st_message' : '',
                'action' : reverse('productos.views.ver_page'),
                'submit_name' : 'Aceptar',
                'title' : 'Crear Producto',
               }
        return render_form(meta, RequestContext(request))
    bodega = int(form.cleaned_data['bodega'])
    categoria = int(form.cleaned_data['categoria'])
    nombre = form.cleaned_data['nombre']

    result = Contenido.objects.all()
    if bodega != -1:
        result = result.filter(bodega=Bodega(bodega))
    if categoria != -1:
        result = result.filter(prod__categoria=Categoria(categoria))
    if nombre:
        result = result.filter(prod__nombre__istartswith=nombre)

    return render_to_response('inventario.html', {'ordenes' : result})

@my_login_required
def modificar_precio_page(request):
    script = """<script type="text/javascript" src="/static/jquery-1.7.2.js" ></script>
        <script type="text/javascript" src="/static/get_cont.js" >
        </script>
        <script type="text/javascript">
            $(document).ready(function () {
                setup();
            });
        </script>"""
    meta = {'method' : 'post',
            'form' : ModificarPrecioForm(),
            'st_message' : script,
            'action' : reverse('productos.views.modificar_precio_page'),
            'submit_name' : 'Guardar',
            'title' : 'Modificar Precio',
           }
    if request.method == 'GET':
        return render_form(meta, RequestContext(request))

    form = ModificarPrecioForm(request.POST)

    if not form.is_valid():
        meta['form'] = form
        return render_form(meta, RequestContext(request))

    nombre = form.cleaned_data['nombre']
    bodega = int(form.cleaned_data['bodega'])
    codigo = form.cleaned_data['codigo']
    cont = Contenido.objects.get(bodega_id=bodega,
                                 prod_id=codigo)
    cont.precio = form.cleaned_data['precio']
    cont.precio2 = form.cleaned_data['precio2']
    cont.cant_mayorista = form.cleaned_data['cantidad_mayorista']
    cont.prod.nombre = nombre
    cont.prod.save()
    cont.save()
    meta['st_message'] += '<p> Precio modificado con exito </p>'
    return render_form(meta, RequestContext(request))


#generar ingreso por Ingreso item
def generar_ingreso_page(ingreso, trans=False):
    ingreso_items = ingreso.ingresoitem_set.all()
    return render_to_response('ver_ingreso.html', {'ingreso' : ingreso,
                                                  'items' : ingreso_items,
                                                  'trans' : trans})

@my_login_required
def transfer_externa_page(request):
    transaction.commit()
    bodegas = Bodega.objects.all().exclude(id=-1)
    bodegas2 = BodegaExterna.objects.all()
    if request.method == 'GET':
        return render_to_response('ingreso.html',
                {'action' : reverse('productos.views.transfer_externa_page'),
                 'bodegas' : bodegas,
                 'bodegas2' : bodegas2,
                 'tipo' : 'E',
                },
                  context_instance=RequestContext(request))
    try:
        codigos = request.POST.getlist('codigo')
        cantidades = request.POST.getlist('cant')
        bodega = int(request.POST['bodega'])
        desde = int(request.POST['desde'])

        items = [(c, p) for p, c in zip(codigos, cantidades) if p != '' and c != '']

        #crear ingreso sin postear
        header = dict(usuario=request.user,
                      bodega_id=desde,
                      tipo=Ingreso.TIPO_EXTERNA)
        callback = lambda c,p : None
        ing = makeIngreso(header, items)

        #hacer el header para enviar alla!
        origen = 'CENTRO: ' + Bodega.objects.get(id=desde).nombre
        header_enviar = dict(origen=origen,
                             entrada=True,
                             numero_externa=ing.id,
                             posteado=False)
        datos = serialize(header_enviar, items)
        url = BodegaExterna.objects.get(id=bodega).url
        num = enviar(url, datos)
        #num = enviar('http://localhost:8000/r/producto/recibir_prod', datos)


        #hacer el ingreso_detalle de aqui!
        bod_ext = BodegaExterna.objects.get(id=bodega)
        detalle = IngresoDetalle(origen=bod_ext.nombre,
                                 ingreso=ing,
                                 entrada=False,
                                 posteado=False,
                                 numero_externa=num
                                 )
        detalle.save()
        transaction.commit()
        if num == -1:
            return HttpResponse("%s no lo recibio bien, el documento \
            esta guardada con numero %d" % (bod_ext.nombre, ing.id))

        return generar_transferencia_externa(ing, RequestContext(request))
    except Exception as x:
        print x, type(x)
        traceback.print_exc()
        transaction.rollback()
        return HttpResponse("fallo la transferencia, problema de ingreso")

def generar_transferencia_externa(ingreso, instance):
    ingreso_items = ingreso.ingresoitem_set.all()
    return render_to_response('ver_trans_externa.html', {'ingreso' : ingreso,
                                                  'items' : ingreso_items,
                                                  'action' : reverse('productos.views.postear_transferencia')
                                                  },
                                                  context_instance=instance)

@my_login_required
def postear_transferencia_form(request, msg=''):
    meta = {'method' : 'get',
            'form' : PosteoForm(),
            'st_message' : msg,
            'action' : reverse('productos.views.postear_transferencia'),
            'submit_name' : 'Ver',
            'title' : 'Postear Form',
           }
    return render_form(meta, None)

@my_login_required
def postear_transferencia(request):
    if request.method == 'GET':
        form = PosteoForm(request.GET)
        if not form.is_valid():
            msg = 'Transferencia codigo %s no existe' % request.GET.get('codigo','')
            return postear_transferencia_form(request, msg)

        codigo = form.cleaned_data['codigo']
        try:
            ing = Ingreso.objects.get(id=codigo)
            if ing.tipo != Ingreso.TIPO_EXTERNA:
                raise Ingreso.DoesNotExist()
        except Ingreso.DoesNotExist:
            msg = 'Transferencia codigo %d no existe' % codigo
            return postear_transferencia_form(request, msg)
        return generar_transferencia_externa(ing, RequestContext(request))

    print request.POST

    form = PosteoForm(request.POST)
    if not form.is_valid():
        return postear_transferencia_form(request)
    codigo = form.cleaned_data['codigo']

    ing = Ingreso.objects.get(pk=codigo)
    items = ing.ingresoitem_set.all()
    detalle = ing.ingresodetalle

    if detalle.posteado:
        return postear_transferencia_form(request, 'Transferencia <b>%d</b> ya fue posteada' % ing.id)

    for i in items:
        if detalle.entrada: #ingreso
            masProd(ing.bodega, i.cantidad, i.producto_id)
        else:
            menosProd(ing.bodega, i.cantidad, i.producto_id)
    detalle.posteado = True
    detalle.fecha_posteo = date.today()
    detalle.aprobado_por = request.user
    detalle.save()
    return postear_transferencia_form(request, 'Transferencia <b>%d</b> posteado con exito' % ing.id)


@my_login_required
def reenviar_trans(request):
    meta = {'method' : 'post',
            'form' : PosteoForm(),
            'st_message' : '',
            'action' : reverse('productos.views.reenviar_trans'),
            'submit_name' : 'Reenviar',
            'title' : 'Reenviar Form',
           }

    if request.method == 'GET':
        return render_form(meta, RequestContext(request))

    form = PosteoForm(request.POST)
    if not form.is_valid():
        meta['st_message'] = 'El documento con codigo <b>%s</b> no existe' % request.POST['codigo']
        meta['form'] = form
        return render_form(meta, RequestContext(request))

    try:
        codigo = form.cleaned_data['codigo']
        ing = Ingreso.objects.get(id=codigo)

        if ing.tipo != Ingreso.TIPO_EXTERNA:
            raise Ingreso.DoesNotExist()

        items = [(str(c.cantidad), c.producto_id) for c in ing.ingresoitem_set.all()]
        origen = 'CENTRO: ' + ing.bodega.nombre
        header_enviar = dict(origen=origen,
                             entrada=True,
                             numero_externa=ing.id,
                             posteado=False)
        datos = serialize(header_enviar, items)
        url = BodegaExterna.objects.get(id=1).url
        num = enviar(url, datos)
        if num != -1:
            detalle = ing.ingresodetalle
            detalle.numero_externa = num
            detalle.save()
            meta['st_message'] = 'Recibio conforme'
        else:
            meta['st_message'] = 'No recibio de nuevo'
    except Ingreso.DoesNotExist:
        meta['st_message'] = 'El documento con codigo <b>%s</b> no existe' % request.POST['codigo']

    return render_form(meta, RequestContext(request))

#---------------------------------------------------------------------------
#Supporting ajax, return JSON
@my_login_required
def get_producto(request):
    try:
        codigo = request.GET['codigo']
        producto=Producto.objects.get(pk=codigo)
        answer = {'status' : True, 'nombre' : producto.nombre }
        data = json.dumps(answer)
        return HttpResponse(data, content_type='application/json')
    except Exception as e:
        print e
        return HttpResponse( json.dumps( {'status' : False }), content_type='application/JSON')


@my_login_required
def get_cont(request):
    try:
        codigo = request.GET['codigo']
        bodega = int(request.GET['bodega'])
        print codigo, bodega
        producto=Contenido.objects.get(prod_id=codigo, bodega_id=bodega)
        answer = {'status' : True,
                  'nombre' : producto.prod.nombre ,
                  'precio' : float(producto.precio),
                  'precio2' : float(producto.precio2),
                  'cant' : float(producto.cant),
                  'cant_mayorista' : producto.cant_mayorista}
        data = json.dumps(answer)
        return HttpResponse(data, content_type='application/json')
    except Exception as e:
        print e
        return HttpResponse( json.dumps( {'status' : False }), content_type='application/JSON')


def buscar_producto(request):
    try:
        codigo = request.GET['codigo']
        bodega = int(request.GET['bodega'])
        print codigo, bodega
        producto=Contenido.objects.filter(prod__nombre__istartswith=codigo, bodega_id=bodega)
        result = [{'codigo' : x.prod_id, 'nombre' : x.prod.nombre} for x in producto]
        answer = {'status' : True,
                  'prod' : result ,
                  }
        data = json.dumps(answer)
        return HttpResponse(data, content_type='application/json')
    except Exception as e:
        print e

@csrf_exempt
def procesar_transferencia(request):
    if request.method == 'GET':
        return HttpResponse()
    try:
        data = request.POST['msg']
        key = request.POST['key']

        if not verificar_crypt(data, key):
            raise Http404

        # esto hay header, y content
        header_rec, content = parse(data)
        header = dict(usuario_id=1,
                      bodega_id=1,
                      tipo='E')
        #content comes with list of (cant, prod)
        #hacer ingreso pero no ingrementar cantidades
        ing = makeIngreso(header, content)

        det = IngresoDetalle(**header_rec)
        det.ingreso = ing
        det.save()
        transaction.commit()
        return HttpResponse(json.dumps({'num' : ing.id}), content_type='application/json')

    except Exception as x:
        print x, type(x)
        traceback.print_exc()
        transaction.rollback()
        raise Http404

