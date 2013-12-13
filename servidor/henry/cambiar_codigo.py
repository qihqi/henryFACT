
from productos.models import *
from facturas.models import *

def cambiar():
    codigos = (
            ('AECHP', 'AECH'),
            ('ARGCB', 'ARCB'),
            ('AAE15', 'AAE1'),
            ('ARAL2.0', 'AAE2'),
            ('AAE20', 'AAE18'),
            ('ALL0.30', 'ALL030'),
            ('ALL0.25', 'ALL025'),
            ('ACXDOC', 'ACX12'),
            ('BAXP', 'BPAR'),
            ('CY18-18', 'CY1818'),
            ('CMETR', 'CINTM'),
            ('CINFIN', 'CINTF'),
            ('CLNFP', 'CLANF'),
            ('CORCO', 'CORTCO'),
            ('CNAB1.56', 'CNAB156'),
            ('CROX12', 'CROCHE'),
            ('ELASTL', 'ELASL'),
            ('ENCAJFI', 'ENCF'),
            ('GALLAVP', 'GLLAVP'),
            ('MARPAR', 'MARGAR'),
            ('MARAFI', 'MAARFI'),
            ('MALLGR', 'MANLGR'),
            ('PVNAT', 'PERVN'),
            ('TCR1.5X2', 'TCR1X2'),
            )
    for inicio, fin in codigos:
        try:
            cambiar_codigo(inicio, fin)
        except Producto.DoesNotExist:
            print 'no se cambio ', inicio, fin

def cambiar_codigo(inicio, fin):
    prod = Producto.objects.get(codigo=inicio)

    for x in prod.ingresoitem_set.all():
        print 'item ingreso numero', x.id, 'cambiado'
        x.producto_id = fin
        x.save()

    for x in prod.itemdeventa_set.all():
        print 'item venta numero', x.id, 'cambiado'
        x.producto_id = fin
        x.save()

    for x in prod.itemdedespacho_set.all():
        print 'item venta numero', x.id, 'cambiado'
        x.producto_id = fin
        x.save()

    #borrar contenidos
    for x in prod.contenido_set.all():
        x.delete()

    print 'borrar producto %s ' % prod.nombre
    prod.delete()
