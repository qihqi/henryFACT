from libros.models import Cuenta

from django import forms
from libros.models import *

class CreateCuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta

class CreateRecordForm(forms.ModelForm):
    tipo = forms.ChoiceField(choices=((1, 'credito'), (-1, 'debito')),
                             widget=forms.RadioSelect)
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Record

class LibroDiarioForm(forms.Form):
    fecha = forms.DateField()

class LibroMayorForm(forms.Form):
    cuenta = forms.ModelChoiceField(queryset=Cuenta.objects.all())
