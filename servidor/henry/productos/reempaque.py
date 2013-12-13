import traceback
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

from main.helper import render_form
from main.views import my_login_required
from main.models import hasNivel

from productos.forms import *
from productos.models import *
from productos.controllers import *
from productos.api import *

@my_login_required
def create_transform_page(request):
    if request.method == 'GET':
        return render_to_response('create_transform.html',
                         {"action" : reverse('productos.reempaque.create_transform_page')},
                          context_instance=RequestContext(request)
                          )

    source = request.POST['source']
    dest = request.POST['dest']
    cant = Decimal(request.POST['mult'])
    if source=='' or dest=='' or cant=='':
        return render_to_response('create_transform.html',
                         {"action" : reverse('productos.reempaque.create_transform_page'),
                          'msg' : 'Todos los campos son requeridos'},
                          context_instance=RequestContext(request)
                          )
    try:
        trans = Transform(origin_id=source,
                          dest_id=dest,
                          multiplier=cant)
        trans.save(force_insert=True)
    except IntegrityError:
        return render_to_response('create_transform.html',
                     {"action" : reverse('productos.reempaque.create_transform_page'),
                      'msg' : 'Regla para %s ya existe!' % source},
                      context_instance=RequestContext(request)
                      )

    return render_to_response('create_transform.html',
                     {"action" : reverse('productos.reempaque.create_transform_page'),
                      'msg' : 'Regla para %s creatado' % source},
                      context_instance=RequestContext(request)
                      )

def ver_reglas_form(request):
    meta = {'method' : 'get',
            'form' : VerProdForm(),
            'st_message' : '',
            'action' : reverse('productos.reempaque.ver_reglas_page'),
            'submit_name' : 'Ver',
            'title' : 'Ver Reglas',
           }
    return render_form(meta, None)

def ver_reglas_page(request):
    form = VerProdForm(request.GET)
    if not form.is_valid():
        meta = {'method' : 'get',
                'form' : form,
                'st_message' : '',
                'action' : reverse('productos.reempaque.ver_reglas_page'),
                'submit_name' : 'Ver',
                'title' : 'Ver Reglas',
               }
        return render_form(meta, None)


    bodega = int(form.cleaned_data['bodega'])
    categoria = int(form.cleaned_data['categoria'])
    nombre = form.cleaned_data['nombre']

    result = Transform.objects.all()
    if categoria != -1:
        result = result.filter(origin__categoria=Categoria(categoria))
    if nombre:
        result = result.filter(origin__nombre__istartswith=nombre)

    url = reverse('productos.reempaque.ver_reglas_page') + '?'
    for key, val in request.GET.iteritems():
        url += key + '=' + val + '%26'
    return render_to_response('ver_reglas.html', {'ordenes' : result,
                                                  'next' : url})

@my_login_required
def modificar_reglas(request):
    if request.method == 'GET':
        codigo = request.GET['codigo']
        return render_to_response('modificar_regla.html',
                   {'codigo' : codigo,
                    'prod' : Transform.objects.get(pk=codigo),
                    'action' : reverse('productos.reempaque.modificar_reglas'),
                    'next': request.GET['next']},
                   context_instance=RequestContext(request))

    if request.POST['action'] == 'Cancelar':
        return HttpResponseRedirect(request.POST['next'])
    codigo = request.POST['codigo']
    regla = Transform.objects.get(pk=codigo)
    regla.multiplier = Decimal(request.POST['mult'])

    regla.save()
    return HttpResponseRedirect(request.POST['next'])

@my_login_required
def reempaque_page(request):
    transaction.commit()
    bodegas = Bodega.objects.all().exclude(id=-1)
    if request.method == 'GET':
        return render_to_response('ingreso.html',
                {'action' : reverse('productos.reempaque.reempaque_page'),
                 'bodegas' : bodegas,
                 'tipo' : 'R',
                },
                  context_instance=RequestContext(request))
    try:
        codigos = request.POST.getlist('codigo')
        cantidades = request.POST.getlist('cant')
        bodega = int(request.POST['bodega'])
        desde = int(request.POST['desde'])

        items = [(Decimal(c), p) for p, c in zip(codigos, cantidades) if p != '' and c != '']

        #crear ingreso sin postear
        header = dict(usuario=request.user,
                      bodega_id=desde,
                      tipo=Ingreso.TIPO_REEMPAQUE)

        callback = functools.partial(menosProd, Bodega(desde))
        ing = makeIngreso(header, items, callback)

        items_r = [transform_prod(c, p) for c, p in items]
        header_r = dict(usuario=request.user,
                      bodega_id=bodega,
                      tipo=Ingreso.TIPO_REEMPAQUE)
        callback2 = functools.partial(masProd, Bodega(bodega))
        ing_r = makeIngreso(header_r, items_r, callback2)

        detalle = IngresoDetalle(origen='REEMPAQUE desde: ' + str( desde),
                                 ingreso=ing,
                                 entrada=False,
                                 posteado=True,
                                 numero_externa=ing_r.id
                                 )
        detalle.save()
        transaction.commit()
        return generar_reempaque(ing, ing_r)

    except Exception as x:
        print x, type(x)
        traceback.print_exc()
        transaction.rollback()
        return HttpResponse("Fallo el reempaque, intente de nuevo ya mismo")


def ver_reempaque(codigo):
    try:
        ing = Ingreso.objects.get(pk=codigo)
        if ing != Ingreso.TIPO_REEMPAQUE:
            return None
        num = ing.ingresodetalle.numero_externa
        ingr = Ingreso.objects.get(pk=num)
        return generar_reempaque(ing, ingr)
    except Ingreso.DoesNotExist:
        return None
    except IngresoDetalle.DoesNotExist:
        return None

def generar_reempaque(ing, ing_r):
    return render_to_response("ver_reempaque.html", {'ing' : ing, 'ingr' : ing_r})

