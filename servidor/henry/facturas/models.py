from django.db import models
from django.contrib.auth.models import User
from clientes.models import Cliente
from productos.models import Producto, Bodega, Contenido
from main.models import UserJava
# Create your models here.

class NotaDeVenta(models.Model):
    vendedor = models.ForeignKey(UserJava)
    cliente = models.ForeignKey(Cliente)
    fecha = models.DateField(auto_now_add=True)
    bodega = models.ForeignKey(Bodega)
    precio_modificado = models.BooleanField()
    class Meta:
        db_table = 'notas_de_venta'


class ItemDeVenta(models.Model):
    venta_cod = models.ForeignKey(NotaDeVenta)
    num = models.IntegerField()
    producto = models.ForeignKey(Producto)
    cantidad = models.DecimalField(max_digits=23, decimal_places=3)
    nuevo_precio = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    @property
    def precio(self):
        if self.nuevo_precio:
            return self.nuevo_precio
        bodega = self.venta_cod.bodega
        cont = Contenido.objects.get(bodega=bodega, prod=self.producto)
        return cont.precio

    def rounded_cant(self):
        return '%.1f' % self.cantidad
    class Meta:
        db_table = 'items_de_venta'
        unique_together = ('venta_cod', 'num')


class OrdenDeDespacho(models.Model):
#esto es factura en menorista
    codigo = models.BigIntegerField()
    bodega = models.ForeignKey(Bodega)
    vendedor = models.ForeignKey(UserJava, db_index=True)
    cliente = models.ForeignKey(Cliente, db_index=True)
    fecha = models.DateField(auto_now_add=True, db_index=True)
    total = models.DecimalField(max_digits=20, decimal_places=2)
    desc = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    pago = models.CharField(max_length=1, db_index=True) #forma de pago
    precio_modificado = models.BooleanField()
    eliminado = models.BooleanField()
    #tipos de pago
    PAGO_EFECTIVO = 'E'
    PAGO_CHEQUE = 'C'
    PAGO_TARGETA = 'T'
    PAGO_DEPOSITO = 'D'
    PAGO_CREDITO = 'R'
    PAGO_VARIOS = 'V'
    class Meta:
        unique_together = ('bodega', 'codigo')
        db_table = 'ordenes_de_despacho'


class ItemDeDespacho(models.Model):
    desp_cod = models.ForeignKey(OrdenDeDespacho)
    num = models.IntegerField()
    producto = models.ForeignKey(Producto)
    cantidad = models.DecimalField(max_digits=23, decimal_places=3)
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    precio_modificado = models.BooleanField()
    def rounded_cant(self):
        return '%.1f' % self.cantidad

    class Meta:
        db_table = 'items_de_despacho'
        unique_together = ('desp_cod', 'num')

class OrdenEliminado(models.Model):
    codigo = models.ForeignKey(OrdenDeDespacho)
    fecha = models.DateField(auto_now_add=True, db_index=True)
    motivo = models.CharField(max_length=200)
    eliminado_por = models.ForeignKey(User)
    class Meta:
        db_table = 'ordenes_eliminados'
