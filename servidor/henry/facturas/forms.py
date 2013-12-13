from django import forms
from main.models import UserJava
from datetime import date
from productos.models import Bodega

class ResumenForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ResumenForm, self).__init__(*args, **kwargs)
        self.fields['vendido_por'].choices = [(v.username, v.username) for v in UserJava.objects.all()]
        self.fields['bodega'].choices = [(v.id, v.nombre) for v in Bodega.objects.all().exclude(id='-1')]

    desde = forms.DateField(initial=date.today())
    hasta = forms.DateField(initial=date.today())
    bodega = forms.ChoiceField(choices=())
    vendido_por = forms.ChoiceField(choices=())

class EliminarForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(EliminarForm, self).__init__(*args, **kwargs)
        self.fields['bodega'].choices = [(v.id, v.nombre) for v in Bodega.objects.all().exclude(id='-1')]

    bodega = forms.ChoiceField(choices=())
    no_de_factura = forms.IntegerField()
    motivo = forms.CharField(widget=forms.Textarea)

class VerDocForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(VerDocForm, self).__init__(*args, **kwargs)
        self.fields['bodega'].choices = [(v.id, v.nombre) for v in Bodega.objects.all().exclude(id='-1')]

    bodega = forms.ChoiceField(choices=())
    codigo = forms.IntegerField()

    CHOICES = (('factura', 'factura'),
               ('nota', 'nota de venta'),
               ('ingreso', 'ingresos'),
               ('reempaque', 'reempaque'),

            )
    tipo = forms.ChoiceField(choices=CHOICES)
