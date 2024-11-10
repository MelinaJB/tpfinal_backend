from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
import pdfplumber
import re
import fitz  # PyMuPDF
from .utils import extraer_datos
from .models import *
from .forms import *


# Create your views here.

#MOSTRAR LISTADO OC + FILTROS
class listadoOC(TemplateView):
    template_name = 'oc/listado_oc.html'
    

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


# class nuevaOC(TemplateView):
#     template_name = 'nueva_oc.html' 
    
#     def get(self, request):
#         pdf_form = PDFUploadForm()
#         oc_form = nuevaOCForm()
#         return render(request, self.template_name, {
#             'pdf_form': pdf_form,
#             'oc_form': oc_form,
#             'extraido': None,
#         })

#     def post(self, request):
#         if 'upload_pdf' in request.POST:
#             # Solo procesar el formulario PDF, pero no guardarlo todavía
#             pdf_form = PDFUploadForm(request.POST, request.FILES)
#             if pdf_form.is_valid():
#                 pdf_instance = pdf_form.save(commit=False)  # No guardar todavía, solo crear la instancia)
#                 datos = extraer_datos(pdf_instance.file.path)
#                 cliente = Cliente.objects.get(cliente=datos.get('uoc'))

#                 print("Datos extraídos:", datos)
                
#                 # Llenar el formulario de la orden de compra con los datos extraídos
#                 oc_form = nuevaOCForm(initial={
#                     'numero': datos.get('numero_orden'),
#                     'fecha': datos.get('fecha_orden'),
#                     'nrocompulsa': datos.get('numero_compulsa'),
#                     'afiliado': datos.get('nombre_afiliado'),
#                     'domicilioafiliado': "Dirección no especificada en el PDF",
#                     'cliente': cliente.id,
#                     'estado': 'pendiente',
#                     'importe_total': datos.get('importe_total')
#                 })

#                 productos = datos.get('detalle_orden', [])
                
#                 print("Productos extraídos:", productos)

#                 return render(request, self.template_name, {
#                     'pdf_form': pdf_form,
#                     'oc_form': oc_form,
#                     'productos': productos,
#                 })
#             else:
#                 return render(request, self.template_name, {
#                     'pdf_form': pdf_form,
#                     'oc_form': nuevaOCForm()
#                 })

#         else:
#             oc_form = nuevaOCForm(request.POST)
#             if oc_form.is_valid():
#                 orden_compra = oc_form.save()
#                 print("Orden de compra guardada:", orden_compra)

#                 productos_data = request.POST.getlist('productos')

#                 cantidad_list = request.POST.getlist('cantidad')
#                 descripcion_list = request.POST.getlist('descripcion')
#                 precio_unitario_list = request.POST.getlist('precio_unitario')

                
#                 # Guardar los productos asociados a la orden de compra
#                 for i in range(len(cantidad_list)):
#                     Producto.objects.create(
#                         orden_compra=orden_compra,
#                         cantidad=cantidad_list[i],
#                         descripcion=descripcion_list[i],
#                         precio_unitario=precio_unitario_list[i]
#                         )
#                     print("Producto guardado:", {
#                         'cantidad': cantidad_list[i],
#                         'descripcion': descripcion_list[i],
#                         'precio_unitario': precio_unitario_list[i]
#                         })
                    
#                 # Guardar el PDF una vez que la orden de compra se guardó
#                 if 'pdf' in request.FILES:
#                     pdf_file = request.FILES['pdf']
#                     pdf_document = PDFDocument.objects.create(
#                         orden_compra=orden_compra,
#                         file=pdf_file
#                     )
#                 print("PDF asociado a la orden de compra:", pdf_document)
                
#                 return redirect('oc:listado_oc')
#             else:
#                 print("Formulario de OC no válido:", oc_form.errors)
        
#         return render(request, self.template_name, {
#             'pdf_form': PDFUploadForm(),
#             'oc_form': oc_form
#         })    


class nuevaOC(TemplateView):
    template_name = 'nueva_oc.html' 
    
    def get(self, request):
        pdf_form = PDFUploadForm()
        oc_form = nuevaOCForm()
        return render(request, self.template_name, {
            'pdf_form': pdf_form,
            'oc_form': oc_form,
            'extraido': None,
        })

    def post(self, request):
        if 'upload_pdf' in request.POST:
            pdf_form = PDFUploadForm(request.POST, request.FILES)
            if pdf_form.is_valid():
                pdf_instance = pdf_form.save()
                datos = extraer_datos(pdf_instance.file.path)
                cliente = Cliente.objects.get(cliente=datos.get('uoc'))

                print("Datos extraídos:", datos)
                
                oc_form = nuevaOCForm(initial={
                    'numero': datos.get('numero_orden'),
                    'fecha': datos.get('fecha_orden'),
                    'nrocompulsa': datos.get('numero_compulsa'),
                    'afiliado': datos.get('nombre_afiliado'),
                    'domicilioafiliado': "Dirección no especificada en el PDF",
                    'cliente': cliente.id,
                    'estado': 'pendiente',
                    'importe_total': datos.get('importe_total')
                })

                productos = datos.get('detalle_orden', [])
                
                print("Productos extraídos:", productos)

                return render(request, self.template_name, {
                    'pdf_form': PDFUploadForm(),
                    'oc_form': oc_form,
                    'productos': productos,
                })
            else:
                return render(request, self.template_name, {
                    'pdf_form': pdf_form,
                    'oc_form': nuevaOCForm()
                })

        else:
            oc_form = nuevaOCForm(request.POST)
            if oc_form.is_valid():
                orden_compra = oc_form.save()
                print("Orden de compra guardada:", orden_compra)

                productos_data = request.POST.getlist('productos')
                cantidad_list = request.POST.getlist('cantidad')
                descripcion_list = request.POST.getlist('descripcion')
                precio_unitario_list = request.POST.getlist('precio_unitario')

                
                # Iterar sobre cada producto extraído y guardarlo en la base de datos
                for i in range(len(cantidad_list)):
                    Producto.objects.create(
                        orden_compra=orden_compra,
                        cantidad=cantidad_list[i],
                        descripcion=descripcion_list[i],
                        precio_unitario=precio_unitario_list[i]
                        )
                    print("Producto guardado:", {
                        'cantidad': cantidad_list[i],
                        'descripcion': descripcion_list[i],
                        'precio_unitario': precio_unitario_list[i]
                        })
                
                return redirect('oc:listado_oc')
            else:
                print("Formulario de OC no válido:", oc_form.errors)
        
        return render(request, self.template_name, {
            'pdf_form': PDFUploadForm(),
            'oc_form': oc_form
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

