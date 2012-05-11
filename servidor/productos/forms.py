from django import forms
from productos.models import *

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Producto

class CreateBodegaForm(forms.ModelForm):
    class Meta:
        model = Bodega

