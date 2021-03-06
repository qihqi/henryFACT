# Create your views here.
from main.models import *
from main.helper import *
from main.forms import *

from django.db import IntegrityError, transaction
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, UserManager
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import user_passes_test

def my_login_required(fn):
#decorator
    def new_func(request, *arg, **kwargs):
        if request.user.is_authenticated():
            return fn(request, *arg, **kwargs)
        else:
            func_name = fn.__name__
            module_name = fn.__module__
            return HttpResponseRedirect('/r/login?next='
                     + reverse(module_name + '.' +func_name))
    return new_func

@my_login_required
def index(request):
    return render_to_response('base.html')

def loginPage(request):
    if request.method == 'GET':
        #return login page
        nextPage = request.GET['next'] if 'next' in request.GET else None
        return render_to_response('login.html', {'form' : AuthenticationForm(),
                                                  'next' : nextPage},
                                   context_instance=RequestContext(request))
    else:
        #do the login and redirect to the desired page
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        nextPage = request.POST['next']
        return HttpResponseRedirect(nextPage)


@my_login_required
@user_passes_test(hasNivel(1), '/r/login')
def createUserPage(request):
    return createUserPageFull(request, True)

@my_login_required
@user_passes_test((lambda u : u.is_staff), '/r/login')
def createUserPageX(request):
    return createUserPageFull(request, False)

def createUserPageFull(request, limited):
    if request.method == 'GET':
        form = CreateUserForm()
        return render_to_response('create_user.html',
                                  {'form' : form,
                                   'duplicado': False,
                                   'creado' : None},
                                  context_instance=RequestContext(request))

    elif request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            try:
                nivel = int(form.cleaned_data['nivel'])
                if limited and nivel > 1:
                    nivel = 1

                createUser(form.cleaned_data['usuario'],
                           form.cleaned_data['clave'],
                           int(form.cleaned_data['nivel']),
                           form.cleaned_data['factura_por'])
                return render_to_response('create_user.html',
                                          {'form' : CreateUserForm(),
                                           'duplicado': False,
                                           'creado' :form.cleaned_data['usuario'] },
                                        context_instance=RequestContext(request)
                        )
            except IntegrityError as e:
                print e
                return render_to_response('create_user.html',
                                      {'form' : form,
                                       'duplicado': True,
                                       'creado' : None},
                                      context_instance=RequestContext(request))
        else:
            return render_to_response('create_user.html',
                                      {'form' : form,
                                       'duplicado': False,
                                       'creado' : None},
                                      context_instance=RequestContext(request))

def get_param_table(additional, params, template):
    template = loader.get_template(template)
    cont = Context({'config' : params})
    return additional + template.render(cont)

@my_login_required
@user_passes_test(hasNivel(1), '/r/login')
def config_page(request):
    form = ConfigForm()
    meta = {'form' : form,
            'method' : 'post',
            'action' : reverse('main.views.config_page'),
            'st_message' : '',
            'submit_name' : 'Guardar',
            'title' : 'Parametros'}
    if request.method == 'GET':

        meta['st_message'] = get_param_table('', Descuento.objects.all(), 'view_config.html')

        return render_form(meta, RequestContext(request))
    #POST
    form = ConfigForm(request.POST)
    if not form.is_valid():
        meta['form'] = form
        return render_form(meta, RequestContext(request))

    #ahora el chiste es valido
    valor = form.cleaned_data['valor']
    param = form.cleaned_data['parametro']

    desc = Descuento.objects.get(pk=param)
    desc.value = valor
    desc.save()

    meta['st_message'] = get_param_table('Parametro <b> %s </b> guardado' % param, Descuento.objects.all(), 'view_config.html')
    meta['form'] = ConfigForm()
    return render_form(meta, RequestContext(request))


@my_login_required
@user_passes_test(hasNivel(1), '/r/login')
def modificar_sequencia_page(request):
    meta = {'form' : SeqForm(),
            'method' : 'post',
            'action' : reverse('main.views.modificar_sequencia_page'),
            'st_message' : '',
            'submit_name' : 'Guardar',
            'title' : 'Modificar Seguencia'}
    if request.method == 'GET':
        meta['st_message'] = get_param_table('', UserJava.objects.all(), 'view_seq.html')
        return render_form(meta, RequestContext(request))

    form = SeqForm(request.POST)
    if not form.is_valid():
        return render_form(meta, RequestContext(request))

    seq = form.cleaned_data['seguencia']
    username = form.cleaned_data['usuario']
    bodega_id = int(form.cleaned_data['bodega'])

    usuario = getUserJava(username)
    usuario.last_factura = seq
    usuario.bodega_factura=Bodega(bodega_id)
    usuario.save()

    msg = 'sequencia para <b> %s </b> cambiado a <b> %d </b>' % (username, seq)
    meta['st_message'] = get_param_table(msg, UserJava.objects.all(), 'view_seq.html')
    meta['form'] = SeqForm()
    return render_form(meta, RequestContext(request))

def test(request):
    #print zip(request.GET.get('codigo',''), request.GET.get('cant'.''))
    return render_to_response('test.html')

@my_login_required
def migration(request):
    if request.method == 'GET':
        return render_to_response('migration.html', context_instance=RequestContext(request))

#    import migration
#    migration.migrarcentro()
    import migration2
    migration2.main()

    return HttpResponse('Migration Complete!')



