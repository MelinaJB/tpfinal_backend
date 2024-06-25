
from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('', index.as_view(), name='index'),
    path('tutoriales/', tutoriales.as_view(), name='tutoriales'),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('login/', loginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
]
