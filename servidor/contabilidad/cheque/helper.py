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
            return HttpResponseRedirect('/c/login?next='
                     + reverse(module_name + '.' +func_name))
    return new_func

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
