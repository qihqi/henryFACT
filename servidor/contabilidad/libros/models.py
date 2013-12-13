from django.db import models

class Cuenta(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=100)
    def __unicode__(self):
        return ' '.join([self.codigo, self.nombre])

class Record(models.Model):
    fecha = models.DateField()
    cuenta = models.ForeignKey(Cuenta)
    valor = models.DecimalField(max_digits=20, decimal_places=2)
    ref_cod = models.CharField(max_length=10)
    ref_detalle = models.CharField(max_length=100)
    def ref_full(self):
        return self.ref_cod + ': ' + self.ref_detalle
    def __unicode__(self):
        return self.ref_detalle
