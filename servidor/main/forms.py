from django import forms

class CreateUserForm(forms.Form):
    usuario = forms.CharField(max_length=50)
    clave = forms.CharField(max_length=20, widget=forms.PasswordInput)
    repetir_clave = forms.CharField(max_length=20, widget=forms.PasswordInput)
    #nivel de permisos
    CHOICES = [ (0 , 'vendedor/cajero'),
                (1 , 'supervisor'),
                (2 , 'administrador')]
    nivel = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
