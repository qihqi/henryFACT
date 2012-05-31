from django import forms
from main.models import Descuento, UserJava


class CreateUserForm(forms.Form):
    usuario = forms.CharField(max_length=50)
    clave = forms.CharField(max_length=20, widget=forms.PasswordInput)
    repetir_clave = forms.CharField(max_length=20, widget=forms.PasswordInput)
    #nivel de permisos
    CHOICES = [ (0 , 'vendedor/cajero'),
                (1 , 'supervisor'),
                (2 , 'administrador')]
    nivel = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

class ConfigForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ConfigForm, self).__init__(*args, **kwargs)
        self.fields['parametro'].choices = [(v.param, v.param) for v in Descuento.objects.all()]

    parametro = forms.ChoiceField(choices=())
    valor = forms.IntegerField()

class SeqForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SeqForm, self).__init__(*args, **kwargs)
        self.fields['usuario'].choices = [(v.username, v.username) for v in UserJava.objects.all()]

    usuario = forms.ChoiceField(choices=())
    seguencia = forms.IntegerField()
