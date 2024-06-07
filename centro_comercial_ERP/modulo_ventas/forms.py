# forms.py
from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'dui', 'telefono', 'correo', 'direccion']
