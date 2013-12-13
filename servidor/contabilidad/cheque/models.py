from django.db import models

# Create your models here.

class Cuenta(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    def __unicode__(self):
        return self.nombre


class Banco(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    def __unicode__(self):
        return self.nombre



class Cheque(models.Model):
    banco = models.ForeignKey(Banco)
    cuenta = models.CharField(max_length=100)
    numero = models.IntegerField()
    titular = models.CharField(max_length=100)

    valor = models.DecimalField(max_digits=20, decimal_places=2)
    fecha = models.DateField()

    fecha_ingreso = models.DateField()
    por_compra = models.CharField(max_length=100, null=True)
    depositado_en = models.ForeignKey(Cuenta, null=True)

    def __unicode__(self):
        return self.titular + ': ' + str(self.valor)

class CambioFecha(models.Model):
    cheque = models.ForeignKey(Cheque)
    fecha_cambiado = models.DateField()
    fecha = models.DateField()
    def __unicode__(self):
        return self.fecha.isoformat()

class Comentario(models.Model):
    cheque = models.ForeignKey(Cheque)
    comentario = models.CharField(max_length=300, null=True)
