# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.db import IntegrityError

from cheque.forms import *
from cheque.helper import *

from datetime import date, timedelta

@my_login_required
def index(request):
    return render_to_response('index.html')

@my_login_required
def create_banco(request):
    form = BancoForm()
    if request.method == 'GET':
        return render_to_response('form.html', {'form' : form,
                                                'action' : reverse('cheque.views.create_banco'),
                                               },
                                  context_instance=RequestContext(request))

    form = BancoForm(request.POST)
    if not form.is_valid():
        return render_to_response('form.html', {'form' : form,
                                                'action' : reverse('cheque.views.create_banco'),
                                               },
                                  context_instance=RequestContext(request))

    try:
        banco = form.save()
    except IntegrityError:
        return render_to_response('form.html', {'form' : form,
                                            'action' : reverse('cheque.views.create_banco'),
                                            'msg' :  'El Banco " %s " ya existe' % banco.nombre,
                                           },
                              context_instance=RequestContext(request))

    return render_to_response('form.html', {'form' : form,
                                            'action' : reverse('cheque.views.create_banco'),
                                            'msg' :  'El Banco " %s " creado' % banco.nombre,
                                           },
                              context_instance=RequestContext(request))
@my_login_required
def create_cheque(request):
    form = ChequeForm(initial={'ingresado_en' : 0})
    if request.method == 'GET':
        return render_to_response('form.html', {'form' : form,
                                                'action' : reverse('cheque.views.create_cheque'),
                                               },
                                  context_instance=RequestContext(request))

    form = ChequeForm(request.POST)
    if not form.is_valid():
        return render_to_response('form.html', {'form' : form,
                                                'action' : reverse('cheque.views.create_cheque'),
                                               },
                                  context_instance=RequestContext(request))

    cheque = form.save(commit=False)
    today = date.today()
    if int(form.cleaned_data['ingresado_en']) == 0:
        cheque.fecha_ingreso = today
    else:
        if today.isoweekday() == 1: #lunes
            cheque.fecha_ingreso = today - timedelta(days=2)
        else:
            cheque.fecha_ingreso = today - timedelta(days=1)


    cheque.save()
    return render_to_response('form.html', {'form' : ChequeForm(),
                                            'action' : reverse('cheque.views.create_cheque'),
                                            'msg' :  'Cheque numero %d ingresado' % cheque.numero,
                                           },
                              context_instance=RequestContext(request))



@my_login_required
def ver_cheques_ingresados(request):
    form = FechaForm(initial={'tipo':'ingresado', 'fecha' : date.today()})
    return render_to_response('form.html', {'form' : form,
                                        'action' : reverse('cheque.views.ver_cheque'),
                                        'method' : 'get'
                                       })

@my_login_required
def ver_cheques_deposito(request):
    form = FechaForm(initial={'tipo':'deposito', 'fecha' : date.today()})
    return render_to_response('form.html', {'form' : form,
                                        'action' : reverse('cheque.views.ver_cheque'),
                                        'method' : 'get'
                                       })
@my_login_required
def ver_cheque(request):
    form = FechaForm(request.GET)
    if not form.is_valid():
        return render_to_response('form.html', {'form' : form,
                                        'action' : reverse('cheque.views.ver_cheque'),
                                })
    tipo = (form.cleaned_data['tipo'] == 'ingresado')
    fecha = form.cleaned_data['fecha']
    query = None
    if tipo:
        query = Cheque.objects.filter(fecha_ingreso=fecha)
    elif fecha.isoweekday() == 1: #si es lunes
        query = Cheque.objects.filter(fecha__lte=fecha, fecha__gte=(fecha - timedelta(days=2)))
    else:
        query = Cheque.objects.filter(fecha=fecha)

    query = list(query)
    total = reduce(lambda x, y : x + y.valor, query, 0)
    return render_to_response('ver_cheques.html',
                              {'ingresado' : tipo,
                               'cheques' : query,
                               'fecha' :fecha.isoformat(),
                               'cuentas' : Cuenta.objects.all(),
                               'next' :reverse('cheque.views.ver_cheque')+\
                                       ('?fecha=' +fecha.isoformat()+ '%26tipo=' + form.cleaned_data['tipo']),

                               'total' : total},
                               context_instance=RequestContext(request))

@my_login_required
def eliminar_cheque(request, id):
    if request.method == 'GET':
        record = Cheque.objects.get(id=id)
        n = request.GET.get('next', '/')
        return render_to_response('eliminar.html',
                                 {'record' : record, 'next' : n},
                                  context_instance=RequestContext(request))

    n = request.POST.get('next', '/c/cheque')
    if request.POST['action'] == 'Cancelar':
        return HttpResponseRedirect(n)

    id = request.POST['id']
    record = Cheque.objects.get(pk=id)
    record.delete()
    return HttpResponseRedirect(n)

@my_login_required
def editar_cheque(request, id):
    if request.method == 'GET':
        n = request.GET.get('next', '')
        record = Cheque.objects.get(id=id)
        form = ChequeForm(instance=record)
        return render_to_response('form.html',
                                 {'form' : form, 'next' : n},
                                  context_instance=RequestContext(request))

    n = request.POST.get('next', '/c/cheque')
    if request.POST['submit'] == 'Cancelar':
        return HttpResponseRedirect(n)
    new_id = int(request.POST.get('id'))
    record = Cheque.objects.get(pk=new_id)
    old_date = record.fecha
    form = ChequeForm(request.POST, instance=record)

    if not form.is_valid():
        return render_to_response('form.html',
                                 {'form' : form, 'next' : n},
                                  context_instance=RequestContext(request))
    if record.fecha != old_date:
        cambio = CambioFecha(cheque=record, fecha=old_date, fecha_cambiado=date.today())
        cambio.save()
    rec = form.save()
    return HttpResponseRedirect(n)

@my_login_required
def depositar(request):
    cheques = request.POST.getlist('cheque')
    dep = request.POST.getlist('deposito')
    for c, d in zip(cheques, dep):
        che = Cheque.objects.get(id=int(c))
        che.depositado_en_id = int(d)
        che.save()

    return HttpResponseRedirect(reverse('cheque.views.index'))

@my_login_required
def ver_cheque_depositados(request):
    form = DoubleFechaForm(request.GET)
    if not form.is_valid():
        return render_to_response('form.html', {'form' : form,
                                        'action' : reverse('cheque.views.ver_cheque_depositados'),
                                        'method' : 'get'
                                       })
    desde = form.cleaned_data['desde']
    if desde.isoweekday() == 1:
        desde = desde - timedelta(days=2)
    elif desde.isoweekday() == 7:
        desde = desde - timedelta(days=1)
    hasta = form.cleaned_data['hasta']

    query = Cheque.objects.filter(fecha__range=(desde, hasta)).exclude(depositado_en=None).order_by('fecha')
    query = list(query)
    total = reduce(lambda x, y : x + y.valor, query, 0)
    return render_to_response('depositado.html', {'query' : query, 'total' : total})

@my_login_required
def ver_cheque_dep_form(request):
    form = DoubleFechaForm(initial={'hasta': date.today(), 'desde' : date.today()})
    return render_to_response('form.html', {'form' : form,
                                        'action' : reverse('cheque.views.ver_cheque_depositados'),
                                        'method' : 'get'

                                        })
@my_login_required
def buscar_cheque_form(request):
    form = BuscarForm()
    return render_to_response('form.html', {'form' : form,
                        'action' : reverse('cheque.views.buscar_cheque'),
                        'method' : 'get'
                        })

@my_login_required
def buscar_cheque(request):
    form = BuscarForm(request.GET)
    if not form.is_valid():
        return render_to_response('form.html', {'form' : form,
                            'action' : reverse('cheque.views.buscar_cheque'),
                                'method' : 'get'
                                })

    desde = form.cleaned_data['desde']
    hasta = form.cleaned_data['desde']
    titular = form.cleaned_data['titular']
    cheque = Cheque.objects.filter(titular__icontains=titular)
    if desde:
        cheque = cheque.filter(fecha__gte=desde)
    if hasta:
        cheque = cheque.filter(fecha__lte=hasta)

    desde = desde.isoformat() if desde else None
    hasta = hasta.isoformat() if hasta else None
    return render_to_response('buscar.html',
                        {
                        'cheques' : cheque,
                        'next' :reverse('cheque.views.buscar_cheque')+\
                        ('?desde=' +str(desde)+ '%26hasta=' + str(hasta)
                         +'%26titular=' + str(titular)
                        ),
                        'total' : ''},
                        )


