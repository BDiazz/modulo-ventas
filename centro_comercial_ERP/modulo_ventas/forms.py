# forms.py
from django import forms
from .models import Cliente
from django import forms
from .models import Servicio, Periodo


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'categoria']

class PeriodoForm(forms.Form):
    periodos = forms.ModelChoiceField(
        queryset=Periodo.objects.all(), 
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Seleccione un período existente'
    )

    def __init__(self, *args, **kwargs):
        super(PeriodoForm, self).__init__(*args, **kwargs)
        self.fields['periodos'].label_from_instance = self.label_from_instance

    def label_from_instance(self, obj):
        return f"{obj.tipo} - ${obj.precio}"
        return f"{obj.tipo} - ${obj.precio}"

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'dui', 'telefono', 'correo', 'direccion']
