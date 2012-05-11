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
        nombres = form.cleaned_data['nombres']
        apellidos = form.cleaned_data['apellidos']
        direccion = form.cleaned_data['direccion']
        codigo = form.cleaned_data['no_de_cedula']
        telefono = form.cleaned_data['telefono']

        client = Cliente(nombres=nombres,
                         apellidos=apellidos,
                         direccion=direccion,
                         codigo=codigo,
                         telefono=telefono)
        client.save()
        meta['st_message'] = 'Cliente <b> %s %s </b> es creado con exito' \
                            % (client.apellidos, client.nombres)
        return render_form(meta, RequestContext(request))
#ver todas las clients
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
def display_client_page(request):
    print " i am called"
    return HttpResponse("hello")

#delete clients
#this does not return a page, handles all by ajax
def delete_client_method(request):
    pass



