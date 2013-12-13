from django.core.management import setup_environ
import sys
sys.path.append('/home/han/Dropbox/servidor-centro/henry')
import settings
setup_environ(settings)
from productos.models import *

from mostSelled import *
from snapshot.heavylifter import *


c = Contenido(prod_id='1234', bodega_id=1)
d = Contenido(prod_id='1234', bodega_id=2)
print  get_ingresados(c)
print  get_ingresados(d)
