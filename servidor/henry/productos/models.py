from django.db import models
from django.contrib.auth.models import User
#(prod, unit, bodega -> precio, cantidad)

class Unidad(models.Model):
    pass

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    def __unicode__(self):
        return self.nombre

    class Meta:
        db_table = 'categorias'

class Producto(models.Model):
    codigo_barra = models.BigIntegerField(null=True) # for later use
    codigo = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, null=True)


    def __unicode__(self):
        return self.nombre
    class Meta:
        db_table = 'productos'

class Bodega(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    nivel = models.IntegerField() #nivel de la bodega
    def __unicode__(self):
        return self.nombre
    class Meta:
        db_table = 'bodegas'

class BodegaExterna(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    url = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.nombre + ' ' + self.url
    class Meta:
        db_table = 'bodegas_externas'


class Contenido(models.Model):
    bodega = models.ForeignKey(Bodega)
    prod = models.ForeignKey(Producto)
    cant = models.DecimalField(max_digits=23, decimal_places=3)
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    precio2 = models.DecimalField(max_digits=20, decimal_places=2)
    cant_mayorista = models.IntegerField(null=True)
    #desde cuando cambia precio

    def __unicode__(self):
        return self.prod.__unicode__()

    def rounded_cant(self): #redondeado a un decimal
        return "%.1f" % self.cant

    class Meta:
        db_table = 'contenido_de_bodegas'
        unique_together = ('bodega', 'prod')

class Ingreso(models.Model):
    fecha = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(User)
    bodega = models.ForeignKey(Bodega)
    bodega_desde = models.ForeignKey(Bodega, null=True, related_name='desde_set')
    tipo = models.CharField(max_length=1)

    TIPO_INGRESO = 'I'
    TIPO_REEMPAQUE = 'R'
    TIPO_EXTERNA = 'E'
    TIPO_TRANSFERENCIA = 'T'
    TIPO_ELIMINADO = 'D'

    def get_related_reempaque(self):
        if self.tipo != Ingreso.TIPO_REEMPAQUE:
            return None

        try:
            num = self.ingresodetalle.numero_externa
            return Ingreso.objects.get(id=num)
        except Exception:
            return None

    class Meta:
        db_table = 'ingresos'

class IngresoItem(models.Model):
    ingreso_cod = models.ForeignKey(Ingreso)
    num = models.IntegerField()
    producto = models.ForeignKey(Producto)
    cantidad = models.DecimalField(max_digits=23, decimal_places=3)

    def rounded_cant(self):
        return "%.1f" % self.cantidad

    class Meta:
        db_table = 'ingreso_items'
        unique_together = ('ingreso_cod', 'num')

class IngresoDetalle(models.Model):
#esta clase solo se usa para detalles de
#transferencia externa, es decir
#si instancia de Ingreso es de tipo 'E'
#tiene que poseer una de esta
    origen = models.CharField(max_length=100)
    ingreso = models.OneToOneField(Ingreso, primary_key=True)
    entrada = models.BooleanField() #Entrada o salida
    numero_externa = models.IntegerField() # que documento corresponde en
    posteado = models.BooleanField()
    fecha_posteo = models.DateField(null=True)
    aprobado_por = models.ForeignKey(User, null=True)

    class Meta:
        db_table = 'ingreso_detalle'



class Transform(models.Model):
    origin = models.OneToOneField(Producto, primary_key=True)
    dest = models.ForeignKey(Producto, related_name='dest_set')
    multiplier = models.DecimalField(max_digits=10, decimal_places=3)

    class Meta:
        db_table = 'transformas'


def transform_prod(cant, prod_id):
#transform that prod into another according to unit
#transformation.
    try:
        trans = Transform.objects.get(origin_id=prod_id)
        new_prod = trans.dest_id
        new_cant = cant * trans.multiplier

        return new_cant, new_prod
    except Transform.DoesNotExist:
        return cant, prod_id
