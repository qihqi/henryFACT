# Create your views here.
from facturas.forms import *
from main.models import UserJava
from main.views import my_login_required
from main.helper import render_form
from main.models import *
from datetime import date
from facturas.models import *

from django.db import IntegrityError, transaction
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, UserManager
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm


#Resumen de venta, la ventana de busqueda
@my_login_required
def resumen_request_page(request):
    #make an empty form
    form = ResumenForm(initial={'desde' : date.today(), 'hasta' : date.today()})
    meta = {'method' : 'get',
            'form' : form,
            'st_message' : '',
            'action' : reverse('facturas.views.generar_resumen_page'),
            'submit_name' : 'Buscar',
            'title' : 'Resumen de Venta',
           }

    return render_form(meta, RequestContext(request))

#parse the request and generate the resume de venta
@my_login_required
def generar_resumen_page(request):
    #necesita privilegio para ver resumen
    print request.user
    if getUserJava(request.user.username).nivel < 2:
        return HttpResponseRedirect('/')

    form = ResumenForm(request.GET)

    if not form.is_valid():
        form = ResumenForm(initial={'desde' : date.today(), 'hasta' : date.today()})
        meta = {'method' : 'get',
                'form' : form,
                'st_message' : 'Datos invalidos',
                'action' : reverse('facturas.views.generar_resumen'),
                'submit_name' : 'Buscar',
                'title' : 'Resumen de Venta',
               }
        return render_form(meta, RequestContext(request))

    desde = form.cleaned_data['desde']
    hasta = form.cleaned_data['hasta']
    vendido = form.cleaned_data['vendido_por']

    resumen = OrdenDeDespacho.objects.filter(fecha__range=(desde, hasta), vendedor=UserJava(username=vendido))

    cheques = list(resumen.filter(pago=OrdenDeDespacho.PAGO_CHEQUE))
    efectivos = list(resumen.filter(pago=OrdenDeDespacho.PAGO_EFECTIVO))
    targetas = list(resumen.filter(pago=OrdenDeDespacho.PAGO_TARGETA))

    cheque_total = sum([c.total for c in cheques])
    print [c.total for c in efectivos]
    efectivo_total = sum([c.total for c in efectivos])
    targeta_total = sum([c.total for c in targetas])

    return render_to_response('resumen.html',
                             {'cheques' : cheques,
                              'efectivos' : efectivos,
                              'targetas' : targetas,
                              'ctotal' : cheque_total,
                              'etotal' : efectivo_total,
                              'ttotal' : targeta_total,
                          })




