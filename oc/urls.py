from django.urls import path
from .views import *

app_name = 'oc'  

urlpatterns = [
    path('listado_oc/', listadoOC.as_view(), name='listado_oc'),
    path('nueva_oc/', nuevaOC.as_view(), name='nueva_oc'),
    path('listado_clientes/', listadoCliente.as_view(), name='listado_clientes'),
    path('nuevo_cliente/', nuevoCliente.as_view(), name='nuevo_cliente'),
]
