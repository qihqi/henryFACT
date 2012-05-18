from django import forms
from main.models import UserJava
from datetime import date

class ResumenForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ResumenForm, self).__init__(*args, **kwargs)
        self.fields['vendido_por'].choices = [(v.username, v.username) for v in UserJava.objects.all()]

    desde = forms.DateField(initial=date.today())
    hasta = forms.DateField(initial=date.today())
    vendido_por = forms.ChoiceField(choices=())

