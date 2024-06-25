from django import forms
from .models import OrdenCompra, Cliente

class nuevaOCForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = '__all__'  
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'  # Puedes especificar los campos específicos si lo prefieres


#class createNewProject(forms.Form):
#    name = forms.CharField(label="Nombre del proyecto", max_length=200, widget=forms.TextInput(attrs={'class': 'input'}))