from django.db import models

from clientes.models import Cliente
from productos.models import Producto, Bodega
from main.models import UserJava
# Create your models here.

class NotasDePedido(models.Model):
    vendedor = models.ForeignKey(UserJava)
    cliente = models.ForeignKey(Cliente)
    fecha = models.DateField(auto_now_add=True)
    bodega = models.ForeignKey(Bodega)
    precio_modificado = models.BooleanField()
    class Meta:
        db_table = 'notas_de_venta'


class ItemDeVenta(models.Model):
    venta_cod = models.ForeignKey(NotasDePedido)
    num = models.IntegerField()
    producto = models.ForeignKey(Producto)
    cantidad = models.IntegerField()
    nuevo_precio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    class Meta:
        db_table = 'items_de_venta'
        unique_together = ('venta_cod', 'num')


class OrdenDeDespacho(models.Model):
#esto es factura en menorista
    codigo = models.BigIntegerField(primary_key=True)
    vendedor = models.ForeignKey(UserJava, db_index=True)
    cliente = models.ForeignKey(Cliente, db_index=True)
    fecha = models.DateField(auto_now_add=True, db_index=True)
    total = models.DecimalField(max_digits=20, decimal_places=2)
    desc = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    bodega = models.ForeignKey(Bodega, db_index=True)
    pago = models.CharField(max_length=1, db_index=True) #forma de pago
    precio_modificado = models.BooleanField()
    eliminado = models.BooleanField()
    #tipos de pago
    PAGO_EFECTIVO = 'E'
    PAGO_CHEQUE = 'C'
    PAGO_TARGETA = 'T'
    class Meta:
        db_table = 'ordenes_de_despacho'


class ItemDeDespacho(models.Model):
    desp_cod = models.ForeignKey(OrdenDeDespacho)
    num = models.IntegerField()
    producto = models.ForeignKey(Producto)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    precio_modificado = models.BooleanField()
    class Meta:
        db_table = 'items_de_despacho'
        unique_together = ('desp_cod', 'num')
