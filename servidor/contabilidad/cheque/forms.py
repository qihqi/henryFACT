from django import forms
from cheque.models import *

class BancoForm(forms.ModelForm):
    class Meta:
        model = Banco
class ChequeForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    por_compra = forms.CharField(required=False)
    ingresado_en = forms.ChoiceField(choices=((0, 'hoy'), (1, 'ayer')), widget=forms.RadioSelect)
    class Meta:
        model = Cheque
        exclude = ('depositado_en',
          'fecha_ingreso'
          )

class FechaForm(forms.Form):
    fecha = forms.DateField()
    tipo = forms.CharField(widget=forms.HiddenInput())

class DoubleFechaForm(forms.Form):
    desde = forms.DateField()
    hasta = forms.DateField()

class BuscarForm(forms.Form):
    titular = forms.CharField()
    desde = forms.DateField(required=False)
    hasta = forms.DateField(required=False)

    def __init__(self, *args, **kwargs):
        super(BuscarForm, self).__init__(*args, **kwargs)
        self.fields['desde'].label = 'Desde(opcional)'
        self.fields['hasta'].label = 'Hasta(opcional)'
