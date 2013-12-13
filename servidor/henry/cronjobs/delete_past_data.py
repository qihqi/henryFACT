from facturas.models import *
from clientes.models import *

from datetime import date, timedelta

def delete_past_data():
    thres = date.today() - timedelta(days=7)
    ventas = NotaDeVenta.objects.filter(fecha__lt=thres)

    for v in ventas:
        print v.id, v.fecha
        v.delete()

    thres = date.today() - timedelta(days=3)
    ventas = NotaDeVenta.objects.filter(fecha__lt=thres, cliente_id='NA')
    for v in ventas:
        print v.id, v.fecha
        v.delete()
