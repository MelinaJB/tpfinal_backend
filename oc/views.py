from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *


# Create your views here.
class Index(TemplateView):
    template_name = 'index'

    def get(self, request):
        title = 'INDEXXXXXX'
        return render(request, 'index.html', {
            'title': title
        })


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


