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

f = open('/home/han/prod_nuevos.txt', 'w')

def dump_prod(item):
    codigo = item['producto']
    x = list(Contenido.objects.filter(prod_id=codigo))
    if len(x) >= 2:
        print >>sys.stderr, x
        return

    print json.dumps(item)


def main():
    with open(sys.argv[1]) as f:
        for x in f.readlines():
            y = json.loads(x)
            dump_prod(y)


main()
f.close()

