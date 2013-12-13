from django.db import models

class Cliente(models.Model):
    codigo = models.CharField(max_length=20, primary_key=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    direccion = models.CharField(max_length=300, null=True)
    ciudad = models.CharField(max_length=50, null=True)
    telefono = models.CharField(max_length=50, null=True)
    tipo = models.CharField(max_length=1)
    cliente_desde = models.DateField(auto_now_add=True)

    @property
    def full(self):
        return self.apellidos + ' ' + self.nombres + '(' +self.codigo + ')'
    @property
    def fullname(self):
        return self.apellidos + ' ' + self.nombres
    def __unicode__(self):
        return self.fullname

    class Meta:
        db_table = 'clientes'
