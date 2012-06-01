from django import forms
from productos.models import *

class CreateProductForm(forms.Form):
    codigo = forms.CharField(max_length=20)
    nombre = forms.CharField(max_length=200, required=False)
    cantidad = forms.IntegerField()
    precio_menorista = forms.DecimalField(max_digits=20, decimal_places=2)
    precio_mayorista = forms.DecimalField(max_digits=20, decimal_places=2)
    bodega = forms.ChoiceField(choices=())

    def __init__(self, *args, **kwargs):
        super(CreateProductForm, self).__init__(*args, **kwargs)
        self.fields['bodega'].choices = [(v.id, v.nombre) for v in Bodega.objects.all()]



class CreateBodegaForm(forms.ModelForm):
    class Meta:
        model = Bodega

