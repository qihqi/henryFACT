from django.db import models
from productos.models import Producto, Bodega, Contenido
from decimal import Decimal
from datetime import date, timedelta

class Snapshot(models.Model):
    fecha = models.DateField()
    bodega = models.ForeignKey(Bodega)
    prod = models.ForeignKey(Producto)
    cant = models.DecimalField(max_digits=13, decimal_places=3, db_index=True)
    venta_cant = models.DecimalField(max_digits=13, decimal_places=3, db_index=True)
    venta_valor = models.DecimalField(max_digits=13, decimal_places=2, db_index=True)
    ingreso_cant = models.DecimalField(max_digits=13, decimal_places=3, db_index=True)
    precio = models.DecimalField(max_digits=13, decimal_places=2)
    precio2 = models.DecimalField(max_digits=13, decimal_places=2)

    @property
    def contenido(self):
        return Contenido.objects.get(bodega_id=self.bodega_id, prod_id=self.prod_id)

    @property
    def avg_precio(self):
        if self.venta_cant:
            return Decimal( "%.2f" % (self.venta_valor / self.venta_cant))
        else:
            return self.precio

    @property
    def fecha_float(self):
        return self.fecha.toordinal()

    @property
    def avg_venta_cant(self):
        if self.get_range().days == 0:
            return self.venta_cant

        return (self.venta_cant / self.get_range().days)

    @property
    def avg_venta_valor(self):
        if self.get_range().days == 0:
            return self.venta_valor
        return Decimal("%.2f" % (self.venta_valor / self.get_range().days))

    def get_range(self):
        lasts = Snapshot.objects.filter( bodega=self.bodega,
                     prod=self.prod, fecha__lt=self.fecha).order_by("-fecha")
        last_fecha = date(2012, 6, 20)
        if lasts.count() != 0:
            last_fecha = lasts[0].fecha
        return self.fecha - last_fecha
    class Meta:
        db_table = 'snapshots'
        unique_together = ('bodega', 'prod', 'fecha')

