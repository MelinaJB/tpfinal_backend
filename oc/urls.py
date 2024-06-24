from django.urls import path
from .views import *

app_name = 'oc'  # Nombre de la aplicación

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('listado_oc/', listadoOC.as_view(), name='listado_oc'),
    # Otras URLs de tu aplicación 'oc' si las tienes
]
