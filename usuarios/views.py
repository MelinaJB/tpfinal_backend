from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
class CustomLoginView(LoginView):
    template_name = 'login.html'

from django.contrib import messages
from .models import *
from .forms import *


# Create your views here.

class index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class tutoriales(TemplateView):
    template_name = 'tutoriales.html'
    def get(self, request):
        tutoriales = tutorialesContenido.objects.all()
        return render(request, 'tutoriales.html', {
            'tutoriales' : tutoriales,
        })

class RegistroView(FormView):
    template_name = 'registro.html'
    form_class = RegistroForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(self.request, user)
        return super().form_valid(form)



class loginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('index')


