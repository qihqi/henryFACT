from django import forms
from main.models import Descuento, UserJava
from productos.models import Bodega


class CreateUserForm(forms.Form):
    usuario = forms.CharField(max_length=50)
    clave = forms.CharField(max_length=20, widget=forms.PasswordInput)
    repetir_clave = forms.CharField(max_length=20, widget=forms.PasswordInput)
    #nivel de permisos
    factura_por = forms.ChoiceField()
    CHOICES = [ (0 , 'vendedor/cajero'),
                (1 , 'supervisor'),
                (2 , 'administrador')]
    nivel = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['factura_por'].choices = [(v.id, v.nombre) for v in Bodega.objects.order_by('id')]


class ConfigForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ConfigForm, self).__init__(*args, **kwargs)
        self.fields['parametro'].choices = [(v.param, v.param) for v in Descuento.objects.order_by('param')]

    parametro = forms.ChoiceField(choices=())
    valor = forms.IntegerField()

class SeqForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SeqForm, self).__init__(*args, **kwargs)
        self.fields['usuario'].choices = [(v.username, v.username) for v in UserJava.objects.order_by('username')]
        self.fields['bodega'].choices = [(v.id, v.nombre) for v in Bodega.objects.order_by('id')]

    usuario = forms.ChoiceField(choices=())
    bodega = forms.ChoiceField()
    seguencia = forms.IntegerField()
