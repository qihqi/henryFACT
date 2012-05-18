# Create your views here.
from facturas.forms import *
from main.models import UserJava
from main.helper import render_form
from datetime import date

from django.db import IntegrityError, transaction
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, UserManager
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm


#Resumen de venta, la ventana de busqueda
def resumen_request_page(request):
    #make an empty form
    form = ResumenForm(initial={'desde' : date.today(), 'hasta' : date.today()})
    meta = {'method' : 'get',
            'form' : form,
            'st_message' : '',
            'action' : reverse('productos.views.create_bodega_page'),
            'submit_name' : 'Buscar',
            'title' : 'Resumen de Venta',
           }

    return render_form(meta, RequestContext(request))

