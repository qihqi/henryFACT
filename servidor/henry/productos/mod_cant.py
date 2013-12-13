import traceback
import json
import functools
from decimal import Decimal
from datetime import date
from django.db import IntegrityError, transaction
from django.core.context_processors import csrf
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, UserManager
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt

from django.core import serializers

from main.helper import render_form
from main.views import my_login_required
from main.models import hasNivel
from productos.forms import *
from productos.models import *
from productos.controllers import *
from productos.api import *

@my_login_required
@user_passes_test(hasNivel(1), '/r/login')
def mod_prod(request):

    if request.method == 'GET':
        return render_to_response('mod_prod.html',
                   {'msg' : '',
                    'bodegas' : Bodega.objects.exclude(id=-1)},
                  context_instance=RequestContext(request))

    bodega = int(request.POST['bodega'])
    codigo = request.POST['codigo']
    cantidad = Decimal(request.POST['cant'])

    cont = Contenido.objects.get(bodega_id=bodega, prod_id=codigo)
    cont.cant = cantidad
    cont.save()

    return render_to_response('mod_prod.html',
                           {'msg' : 'producto %s modificado' % codigo,
                            'bodegas' : Bodega.objects.exclude(id=-1)},
                           context_instance=RequestContext(request))
