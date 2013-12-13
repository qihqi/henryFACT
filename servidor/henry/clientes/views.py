from django.db import IntegrityError, transaction
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, UserManager
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from main.helper import render_form
from main.views import my_login_required
from clientes.forms import *
from clientes.models import *
#Crear cliente, update cliente
#futuro: manejo de deudas y creditos

@my_login_required
def create_client_page(request):
    form = CreateClientForm()
    meta = {'method' : 'post',
            'form' : form,
            'st_message' : '',
            'action' : reverse('clientes.views.create_client_page'),
            'submit_name' : 'Crear',
            'title' : 'Crear Cliente',
           }
    if request.method == 'GET':
        return render_form(meta, RequestContext(request))

    elif request.method == 'POST':
    #process the data, redirect to itself.
        form = CreateClientForm(request.POST)
        if not form.is_valid():
            meta['form'] = form
            return render_form(meta, RequestContext(request))
        #ahora es valid
        client = form.save()
        meta['st_message'] = 'Cliente <b> %s %s </b> es creado con exito' \
                            % (client.apellidos, client.nombres)
        return render_form(meta, RequestContext(request))

@my_login_required
def editar_cliente_page(request, codigo):
    meta = {'method' : 'post',
            'form' : None,
            'st_message' : '',
            'action' : reverse('clientes.views.editar_cliente_page', kwargs={'codigo' : codigo}),
            'submit_name' : 'Guardar',
            'title' : 'Editar Cliente',
           }
    if request.method == 'GET':
        c = Cliente.objects.get(codigo=codigo)
        form = CreateClientForm(instance=c, initial={'codigo_embedded' : codigo})
        meta['form'] = form
        return render_form(meta, RequestContext(request))

    cod_true = request.POST.get('codigo_embedded', None)

    cod = request.POST['codigo']

    if cod_true == None:
        meta['st_message'] = 'cliente no fue modificado'
        return render_form(meta, RequestContext(request))
    if cod_true != cod:
        meta['st_message'] = 'No se puede cambiar la numero de cedula, \
                              \n Crea otro cliente!'
        return render_form(meta, RequestContext(request))

    c = Cliente.objects.get(codigo=cod_true)
    form = CreateClientForm(request.POST, instance=c)
    if not form.is_valid():
        meta['form'] = form
        return render_form(meta, RequestContext(request))
    form.save()

    meta['st_message'] = 'cliente modificado'
    meta['form'] = form
    return render_form(meta, RequestContext(request))


@my_login_required
def eliminar_cliente_page(request,codigo):
    if request.method == 'GET':
        c = Cliente.objects.get(codigo=codigo)
        return render_to_response('eliminar_cliente.html', {'codigo' : codigo, 'cliente' : c.fullname},
                                  context_instance=RequestContext(request))

    codigo = request.POST['codigo']
    action = request.POST['action']
    if action == 'Cancelar':
        return HttpResponseRedirect(reverse('clientes.views.search_client_page'))

    cliente = Cliente.objects.get(codigo=codigo)

    for x in cliente.ordendedespacho_set.all():
        x.cliente_id = '00'
        x.save()

    for x in cliente.notadeventa_set.all():
        x.cliente_id = '00'
        x.save()


    nombre = cliente.fullname
    cliente.delete()

    return render_to_response('eliminado.html', {'cliente' : nombre})

#ver todas las clients
@my_login_required
def search_client_page(request):
    form = SearchClientForm()
    meta = {'method' : 'get',
            'form' : form,
            'st_message' : '',
            'action' : reverse('clientes.views.display_client_page'),
            'submit_name' : 'Buscar',
            'title' : 'Buscar Cliente',
           }

    return render_form(meta, None)

#display clients
@my_login_required
def display_client_page(request):
    apellidos = request.GET['apellidos']
    query = Cliente.objects.filter(apellidos__istartswith=apellidos)
    form = SearchClientForm()
    return render_to_response('all_cliente.html', {'clientes' : query,
                                                   'form' : form,
                                                   'action' :  reverse('clientes.views.display_client_page')})

#delete clients
#this does not return a page, handles all by ajax

