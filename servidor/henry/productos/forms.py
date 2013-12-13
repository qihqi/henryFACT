from django import forms
from productos.models import *

class PosteoForm(forms.Form):
    codigo = forms.IntegerField()


class CreateProductForm(forms.Form):
    codigo = forms.CharField(max_length=20)
    nombre = forms.CharField(max_length=200, required=False)
    precio_menorista = forms.DecimalField(max_digits=20, decimal_places=2)
    precio_menorista_2 = forms.DecimalField(max_digits=20, decimal_places=2)
    precio_mayorista = forms.DecimalField(max_digits=20, decimal_places=2)
    precio_mayorista_2 = forms.DecimalField(max_digits=20, decimal_places=2)
   # bodega = forms.ChoiceField(choices=())
    categoria = forms.ChoiceField(choices=())

    def __init__(self, *args, **kwargs):
        super(CreateProductForm, self).__init__(*args, **kwargs)
    #    self.fields['bodega'].choices = [(v.id, v.nombre) for v in Bodega.objects.all().exclude(id=-1)]
        self.fields['categoria'].choices = [(v.id, v.nombre) for v in Categoria.objects.all()]

class VerProdForm(forms.Form):
    bodega = forms.ChoiceField()
    categoria = forms.ChoiceField()

    nombre = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(VerProdForm, self).__init__(*args, **kwargs)
        self.fields['bodega'].choices = [(-1, 'Todas')] + [(v.id, v.nombre) for v in Bodega.objects.all().exclude(id=-1)]
        self.fields['categoria'].choices = [(-1, 'Todas')] + [(v.id, v.nombre) for v in Categoria.objects.all()]


class ModificarPrecioForm(forms.Form):
    bodega = forms.ChoiceField()
    codigo = forms.CharField(max_length=20)
    nombre = forms.CharField()
    precio = forms.DecimalField()
    precio2 = forms.DecimalField()
    cantidad_mayorista = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super(ModificarPrecioForm, self).__init__(*args, **kwargs)
        self.fields['bodega'].choices =  [(v.id, v.nombre) for v in Bodega.objects.all().exclude(id=-1)]

class CreateBodegaForm(forms.ModelForm):
    class Meta:
        model = Bodega

class CreateCatForm(forms.ModelForm):
    class Meta:
        model = Categoria
