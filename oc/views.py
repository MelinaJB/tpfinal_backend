from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import *
from .forms import *


# Create your views here.

#MOSTRAR LISTADO OC + FILTROS
class listadoOC(TemplateView):
    template_name = 'oc/listado_oc.html'
    
#    @method_decorator(@login_required())
    def get(self, request):
        estado = request.GET.get('estado', None)
        numero = request.GET.get('numero', "")
        
        # Construir el queryset filtrado en base a los filtros aplicados
        queryset = OrdenCompra.objects.all()
        
        if estado:
            queryset = queryset.filter(estado=estado)
        
        if numero:
            queryset = queryset.filter(numero__icontains=numero)  # o usar el campo adecuado
        
        # Obtener todos los estados únicos
        filtro_estados = OrdenCompra.objects.values_list('estado', flat=True).distinct()
        
        return render(request, 'listado_oc.html', {
            'listado': queryset,
            'filtro_estados': filtro_estados,
            'estado_seleccionado': estado,
            'numero_seleccionado': numero
        })

#CREAR NUEVA ORDEN DE COMPRA
#@login_required(login_url="login")
class nuevaOC(TemplateView):
    template_name = 'nueva_oc'
    
    def get(self, request):
        form = nuevaOCForm()
        return render(request, 'nueva_oc.html', {
            'form': form
            })
    
    def post(self, request):
        form = nuevaOCForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('oc:listado_oc')
        return render(request, 'listado_oc.html', {
            'form': form
            })
    
#MODIFICAR OC
class modificarOC(TemplateView):
    def get(self, request, id):
        nroid = OrdenCompra.objects.get(pk = id)
        form = nuevaOCForm(instance=nroid)
        return render(request, 'modificar_oc.html',{
            'nroid' : nroid,
            'form': form
        })
    
    def post(self, request, id):
        oc = get_object_or_404(OrdenCompra, pk=id)
        form = nuevaOCForm(request.POST, instance=oc)
        if form.is_valid():
            form.save()
            return redirect('oc:listado_oc')
        return render(request, 'modificar_oc.html', {
            'nroid': oc,
            'form': form
        })

#MOSTRAR LISTADO DE CLIENTES REGISTRADOS
class listadoCliente(TemplateView):
    template_name = 'oc/listado_cliente.html'

    def get(self, request):
        cliente = Cliente.objects.all()
        return render(request, 'listado_clientes.html', {
            'cliente': cliente
        })


#CREAR NUEVO CLIENTE
class nuevoCliente(TemplateView):
    template_name = 'nuevo_cliente.html'
    
    def get(self, request):
        form = ClienteForm()
        return render(request, 'nuevo_cliente.html', {
            'form': form
            })
    
    def post(self, request):
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('oc:listado_clientes')
        return render(request, self.template_name, {'form': form})