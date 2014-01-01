from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test

from main.views import my_login_required
from main.models import hasNivel
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
