from django.core.management import setup_environ
from django.db import transaction
import sys
sys.path.append('/var/servidor/henry')
import settings
setup_environ(settings)

from facturas.models import *
from decimal import Decimal
import datetime
import json

def fix_cliente(inv):
    cliente = Cliente.objects.filter(codigo=inv['cliente'])
    if not cliente:
        print 'crear cliente'
        cliente = Cliente(**inv['cliente_detalle'])
        cliente.save()


def main():
    with open(sys.argv[1]) as f:
        for x in f.readlines():
            for y in json.loads(x)['items']:
                fix_cliente(y)


main()
