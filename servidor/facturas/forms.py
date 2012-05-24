from django import forms
from main.models import UserJava
from datetime import date
from productos.models import Bodega

class ResumenForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ResumenForm, self).__init__(*args, **kwargs)
        self.fields['vendido_por'].choices = [(v.username, v.username) for v in UserJava.objects.all()]
        self.fields['bodega'].choices = [(v.id, v.nombre) for v in Bodega.objects.all()]

    desde = forms.DateField(initial=date.today())
    hasta = forms.DateField(initial=date.today())
    bodega = forms.ChoiceField(choices=())
    vendido_por = forms.ChoiceField(choices=())

