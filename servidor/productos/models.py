from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    codigo = models.CharField(max_length=20, primary_key=True)
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    nombre = models.CharField(max_length=200)
    def __unicode__(self):
        return self.nombre
    class Meta:
        db_table = 'productos'

class Bodega(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    def __unicode__(self):
        return self.nombre
    class Meta:
        db_table = 'bodegas'

class Contenido(models.Model):
    bodega = models.ForeignKey(Bodega)
    prod = models.ForeignKey(Producto)
    cant = models.IntegerField()
    class Meta:
        db_table = 'contenido_de_bodegas'
        unique_together = ('bodega', 'prod')

class Ingreso(models.Model):
    fecha = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(User)
    bodega = models.ForeignKey(Bodega)
    class Meta:
        db_table = 'ingresos'

class IngresoItem(models.Model):
    ingreso_cod = models.ForeignKey(Ingreso)
    num = models.IntegerField()
    producto = models.ForeignKey(Producto)
    cantidad = models.IntegerField()
    class Meta:
        db_table = 'ingreso_items'
        unique_together = ('ingreso_cod', 'num')
