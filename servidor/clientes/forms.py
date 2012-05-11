from django import forms

class CreateClientForm(forms.Form):
    nombres = forms.CharField(max_length=100)
    apellidos = forms.CharField(max_length=100)
    direccion = forms.CharField(max_length=300)
    no_de_cedula = forms.CharField(max_length=50)
    telefono = forms.CharField(max_length=50)

class SearchClientForm(forms.Form):
    nombres = forms.CharField(max_length=100)
    apellidos = forms.CharField(max_length=100)


