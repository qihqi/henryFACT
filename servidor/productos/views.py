# Create your views here.
import json
from django.db import IntegrityError, transaction
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, UserManager
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from django.core import serializers

from main.helper import render_form
from main.views import my_login_required
from productos.forms import *
from productos.models import *

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
    data = form.cleaned_data
    bodega = Bodega(nombre=data['nombre'])

    bodega.save()

    meta['st_message'] = 'Bodega <b> %s </b> es creado con exito' % bodega.nombre
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
    print data
    prod = Producto(nombre=nombre, codigo=codigo)
    try:
        prod.save()
    except IntegrityError:
        prod = Producto.objects.get(codigo=codigo)
        if nombre != '' and prod.nombre != nombre:
            meta['st_message'] = 'El codigo <b> %s </b> ya esta usado \
                                  para el producto <b> %s </b>; <br /> \
                                  Utilice otro codigo o deje el nombre libre.' % (codigo, prod.nombre)
            transaction.rollback()
            return render_form(meta, RequestContext(request))

    print data

    #Crear transaction
    try:
        cont = Contenido(prod=prod,
                         precio=data['precio_menorista'],
                         precio2=data['precio_mayorista'],
                         bodega=Bodega(data['bodega']),
                         cant=data['cantidad'])
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
        print post
        codigos = post.getlist('codigo')
        cantidades = post.getlist('cant')
        bodega = post['bodega']
        #if len(codigos) != len(cantidades):
        #    raise Exception()
        for x in cantidades:
            if x != '':
                int(x)
        int(bodega)
        return True
    except Exception as x:
        print x, type(x)
        return False

@my_login_required
def ingreso_producto_page(request):
    transaction.commit()
    bodegas = Bodega.objects.all()
    if request.method == 'GET':
        return render_to_response('ingreso.html',
                {'action' : reverse('productos.views.ingreso_producto_page'),
                 'bodegas' : bodegas},
                  context_instance=RequestContext(request))

    #insert the ingreso de bodega
    #transaction handled by middleware
    if not validate_ingreso(request.POST):
        return HttpResponse("hola")

    codigos = request.POST.getlist('codigo')
    cantidades = request.POST.getlist('cant')
    bodega = int(request.POST['bodega'])
    ingreso = Ingreso(usuario=request.user,
                      bodega_id=bodega )
    ingreso.save()
    #ingresar items:
    for i, (cod, cant) in enumerate(zip(codigos, cantidades)):
        if cod != '' and cant != '':

            #si existe en contenido, lo suma
            #sino lo crea y asigna la cantidad
            content, created = Contenido.objects.get_or_create(
                                bodega_id=bodega,
                                prod_id=cod,
                                defaults={'cant': cant})
            if not created:
                content.cant += int(cant)
                content.save()

            #crear y guardar ingreso
            item = IngresoItem(ingreso_cod=ingreso,
                               producto_id=cod,
                               cantidad=int(cant),
                               num=i)
            item.save()

    #retornando no matter what
    return render_to_response('ingreso.html',
            {'action' : reverse('productos.views.ingreso_producto_page'),
             'bodegas' : bodegas},
              context_instance=RequestContext(request))

@my_login_required
def ver_producto_page(request):

    return render_to_response('inventario.html', {'ordenes' : Producto.objects.all()});

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





