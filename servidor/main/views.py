# Create your views here.
from main.models import *
from main.forms import *

from django.db import IntegrityError, transaction
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, UserManager
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

def my_login_required(fn):
#decorator
    def new_func(request, *arg, **kwargs):
        if request.user.is_authenticated():
            return fn(request, *arg, **kwargs)
        else:
            func_name = fn.__name__
            module_name = fn.__module__
            return HttpResponseRedirect('/login?next='
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
def createUserPage(request):
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
                createUser(form.cleaned_data['usuario'],
                           form.cleaned_data['clave'],
                           int(form.cleaned_data['nivel']))
                return render_to_response('create_user.html',
                                          {'form' : CreateUserForm(),
                                           'duplicado': False,
                                           'creado' :form.cleaned_data['usuario'] },
                                        context_instance=RequestContext(request)
                        )
            except IntegrityError:
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
def test(request):
    #print zip(request.GET.get('codigo',''), request.GET.get('cant'.''))
    return render_to_response('test.html')


