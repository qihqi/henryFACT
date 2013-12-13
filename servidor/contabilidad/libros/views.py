# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from libros.helper import *
from libros.forms import *
from cheque.helper import *
import math
@my_login_required
def index(request):
    return render_to_response('base.html')

@my_login_required
def create_cuenta_page(request):
    meta = {'form' : CreateCuentaForm(),
            'method' : 'post',
            'action' : reverse('libros.views.create_cuenta_page'),
            'st_message' : '',
            'submit_name' : 'Guardar',
            'title' : 'Ingresar Cuenta'}
    if request.method == 'GET':
        return render_form(meta, RequestContext(request))

    form = CreateCuentaForm(request.POST)
    if not form.is_valid():
        meta['form'] = form
        return render_form(meta, RequestContext(request))

    cuenta = form.save()
    meta['st_message'] = 'Cuenta <b> %s %s </b> creado con exito' % (cuenta.codigo, cuenta.nombre)
    return render_form(meta, RequestContext(request))

@my_login_required
def create_record_page(request):
    print 'called'
    meta = {'form' : CreateRecordForm(),
            'method' : 'post',
            'action' : reverse('libros.views.create_record_page'),
            'st_message' : '',
            'submit_name' : 'Guardar',
            'title' : 'Ingresar Record'}
    if request.method == 'GET':
        print 'get'
        return render_form(meta, RequestContext(request))

    form = CreateRecordForm(request.POST)
    if not form.is_valid():
        meta['form'] = form
        return render_form(meta, RequestContext(request))
    record = form.save(commit=False)
    valor = abs(record.valor) * int(form.cleaned_data['tipo'])
    record.valor = valor
    record.save()
    meta['st_message'] = 'Record %s fue guardada' % record.ref_detalle
    return render_form(meta, RequestContext(request))


@my_login_required
def ver_libro_mayor_form(request):
    meta = {'form' : LibroMayorForm(),
            'method' : 'get',
            'action' : reverse('libros.views.ver_libro_mayor_page'),
            'st_message' : '',
            'submit_name' : 'Guardar',
            'title' : 'Ingresar Record'}
    return render_form(meta, RequestContext(request))

@my_login_required
def ver_libro_mayor_page(request):
    form = LibroMayorForm(request.GET)
    if not form.is_valid():
        meta = {'form' : form,
                'method' : 'get',
                'action' : reverse('libros.views.ver_libro_mayor_page'),
                'st_message' : '',
                'submit_name' : 'Guardar',
                'title' : 'Ingresar Record'}
        return render_form(meta, RequestContext(request))

    cuenta = form.cleaned_data['cuenta']
    records = list(Record.objects.filter(cuenta=cuenta))
    total = reduce(lambda x, y : x + y.valor, records, 0)
    sign = (total > 0)
    return render_to_response('mayor.html', {'records' : records, 'total' : abs(total), 'sign' : sign})

@my_login_required
def ver_libro_diario_form_page(request):
    meta = {'form' : LibroDiarioForm(),
            'method' : 'get',
            'action' : reverse('libros.views.ver_libro_diario_page', kwargs={'impresion' : 0}),
            'st_message' : '',
            'submit_name' : 'Guardar',
            'title' : 'Ingresar Record'}
    return render_form(meta, RequestContext(request))


@my_login_required
def ver_libro_diario_page(request, impresion):
    form = LibroDiarioForm(request.GET)
    if not form.is_valid():
        meta = {'form' : form,
                'method' : 'get',
                'action' : reverse('libros.views.ver_libro_diario_page', kwargs={'impresion' : 0}),
                'st_message' : '',
                'submit_name' : 'Guardar',
                'title' : 'Ingresar Record'}
        return render_form(meta, RequestContext(request))

    fecha = form.cleaned_data['fecha']
    records = list(Record.objects.filter(fecha=fecha))
    impre = (int(impresion) == 1)
    credito = 0
    debito = 0
    for r in records:
        if r.valor > 0:
            credito += r.valor
        else:
            debito += abs(r.valor)

    return render_to_response('diario.html',
                             {'records' : records,
                                 'next' : (reverse('libros.views.ver_libro_diario_page', kwargs={'impresion' : 0})
                                           +"?fecha="+request.GET['fecha']),
                               'credito' : credito,
                               'debito' : debito,
                               'impresion' : impre
                             },
                              context_instance=RequestContext(request)
                             )

@my_login_required
def eliminar_record_page(request, id):
    if request.method == 'GET':
        record = Record.objects.get(id=id)
        n = request.GET.get('next', '/')
        return render_to_response('eliminar_form.html',
                                 {'record' : record, 'next' : n},
                                  context_instance=RequestContext(request))

    n = request.POST.get('next', '/')
    if request.POST['action'] == 'Cancelar':
        return HttpResponseRedirect(n)

    id = request.POST['id']
    record = Record.objects.get(pk=id)
    record.delete()
    return HttpResponseRedirect(n)

@my_login_required
def editar_record_page(request, id):
    record = Record.objects.get(id=id)
    form = CreateRecordForm(instance=record)
    meta = {'form' : form,
            'method' : 'post',
            'action' : reverse('libros.views.editar_record_page', kwargs={'id' : id}),
            'st_message' : '',
            'submit_name' : 'Guardar',
            'title' : 'Editar Record'}

    if request.method == 'GET':
        sign = 1 if form.initial['valor'] > 0 else -1
        form.initial['valor'] = abs(form.initial['valor'])
        form.initial['tipo'] = sign

        n = request.GET.get('next', '')
        meta['next'] = n
        return render_form(meta, RequestContext(request))

    if request.POST['action'] == 'Cancelar':
        return HttpResponseRedirect(n)

    new_id = int(request.POST.get('id'))
    record = Record.objects.get(pk=new_id)
    form = CreateRecordForm(request.POST, instance=record)

    if not form.is_valid():
        meta['form'] = form
        return render_form(meta, RequestContext(request))

    rec = form.save(commit=False)
    valor = abs(rec.valor) * int(form.cleaned_data['tipo'])
    rec.valor = valor
    rec.save()
    n = request.POST.get('next', '/contab')
    return HttpResponseRedirect(n)

@my_login_required
def ver_cuenta(request):
    return render_to_response('all_cuenta.html',
             {'query' : Cuenta.objects.all() })
@my_login_required
def editar_cuenta(request):
    form = CreateCuentaForm()
    meta = {'form' : form,
           'method' : 'post',
           'action' : reverse('libros.views.editar_cuenta'),
           'st_message' : '',
           'submit_name' : 'Guardar',
           'title' : 'Editar Cuenta'}


    if request.method == 'GET':
        codigo = request.GET['codigo']
        obj = Cuenta.objects.get(codigo=codigo)
        form = CreateCuentaForm(instance=obj)
        meta['form'] = form
        return render_form(meta, RequestContext(request))


    codigo = request.POST['codigo']
    nombre = request.POST['nombre']

    cuenta = None
    try:
        cuenta = Cuenta.objects.get(codigo=codigo)
    except Cuenta.DoesNotExist:
        query = list(Cuenta.objects.filter(codigo__startswith=codigo))
        if not query:
            meta['st_message'] = 'Cuenta %s no existe' % codigo
            return render_form(meta, RequestContext(request))

        cuenta = query[0]

    cuenta.nombre = nombre
    cuenta.save()

    meta['st_message'] = 'Cuenta %s cambiado a %s' % (cuenta.codigo, cuenta.nombre)
    return render_form(meta, RequestContext(request))
