from django import forms
from clientes.models import Cliente

class CreateClientForm(forms.ModelForm):
    tipo = forms.ChoiceField(choices=(('A', 'Menorista'),('B', 'Mayorista')),
                             widget=forms.RadioSelect)

    codigo_embedded = forms.CharField(widget=forms.HiddenInput(), required=False)
    def __init__(self, *args, **kwargs):
        super(CreateClientForm, self).__init__(*args, **kwargs)
        self.fields['codigo'].label = 'No de Cedula'

    class Meta:
        model = Cliente

class SearchClientForm(forms.Form):
    apellidos = forms.CharField(max_length=100)


