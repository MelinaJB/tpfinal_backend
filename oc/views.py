from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import *
from .forms import *


# Create your views here.
class panelUsuarios(TemplateView):
    template_name = 'panelusuarios'
    def get(self, request):
        return render (request, 'usuarios.html')

#MOSTRAR LISTADO OC + FILTROS
class listadoOC(TemplateView):
    template_name = 'oc/listado_oc.html'

    def get(self, request):
        estado = request.GET.get('estado', None)
        numero = request.GET.get('numero', None)
        
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
            return redirect('oc:listado_clientes')  # Cambia 'listado_clientes' por la URL de tu lista de clientes
        return render(request, self.template_name, {'form': form})