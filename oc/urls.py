from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

app_name = 'oc'  

urlpatterns = [
    path('listado_oc/', login_required(listadoOC.as_view()), name='listado_oc'),
    path('nueva_oc/', login_required(nuevaOC.as_view()), name='nueva_oc'),
    path('modificar_oc/<int:id>/', login_required(modificarOC.as_view()), name='modificar_oc'),
    path('listado_clientes/', login_required(listadoCliente.as_view()), name='listado_clientes'),
    path('nuevo_cliente/', login_required(nuevoCliente.as_view()), name='nuevo_cliente'),
    path('subir_pdf/', login_required(PDFUploadView.as_view()), name='subir_pdf'),
]
