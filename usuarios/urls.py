
from django.urls import path
from .views import *

urlpatterns = [
    path('', index.as_view(), name='index'),
    path('tutoriales/', tutoriales.as_view(), name='tutoriales'),
    path('registro/', RegistroView.as_view(), name='registro'),
]
