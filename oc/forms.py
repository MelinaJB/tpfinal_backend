from django import forms
from .models import *



class nuevaOCForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = '__all__'  
        widgets = {
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nrocompulsa': forms.NumberInput(attrs={'class': 'form-control'}),
            'afiliado': forms.TextInput(attrs={'class': 'form-control'}),
            'domicilioafiliado': forms.TextInput(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'entrega_unica': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'numero': 'Número de Orden',
            'fecha': 'Fecha de la Orden',
            'nrocompulsa': 'Número de Compulsa',
            'afiliado': 'Afiliado',
            'domicilioafiliado': 'Domicilio de Entrega',
            'cliente': 'Cliente',
            'estado': 'Estado',
            'entrega_unica': 'Entrega Única',
        }


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'  # Puedes especificar los campos específicos si lo prefieres
        widgets = {
            'cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'cuit': forms.TextInput(attrs={'class': 'form-control'}),
            'domiciliocliente': forms.TextInput(attrs={'class': 'form-control'}),
        }

