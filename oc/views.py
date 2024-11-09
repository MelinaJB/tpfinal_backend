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

    
class nuevaOC(TemplateView):
    template_name = 'nueva_oc.html' 
    
    def get(self, request):
        # Formularios vacíos para subir el PDF y crear una nueva orden de compra
        pdf_form = PDFUploadForm()
        oc_form = nuevaOCForm()
        return render(request, self.template_name, {
            'pdf_form': pdf_form,
            'oc_form': oc_form,
            'extraido': None,
        })
    
  
    def post(self, request):
        # Si se está enviando el formulario de subida del PDF
        if 'upload_pdf' in request.POST:
            pdf_form = PDFUploadForm(request.POST, request.FILES)
            if pdf_form.is_valid():
                # Guardar el PDF y extraer datos
                pdf_instance = pdf_form.save()
                datos = extraer_datos(pdf_instance.file.path)
                cliente = Cliente.objects.get(cliente=datos.get('uoc'))

                # print(datos)
                
                # Configurar los valores extraídos como iniciales para el formulario de nueva orden de compra
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

                # ESTO LO ESTOY AGREGANDO AHORA
                # Extraer datos de productos del detalle de la orden
                cantidades = re.findall(r'^\s*(\d+)', datos.get('detalle_orden'), re.MULTILINE)
                descripciones = re.findall(r'([A-Z\s]+)', datos.get('detalle_orden'))
                precios_unitarios = re.findall(r'\d{1,3}(?:\.\d{3})*,\d{2}', datos.get('detalle_orden'))
                # cantidades = re.findall(r'\b\d+\b', datos.get('detalle_orden'))
                # descripciones = re.findall(r'[A-Z\s]+', datos.get('detalle_orden'))
                # precios_unitarios = re.findall(r'\d{1,3}(?:\.\d{3})*,\d{2}', datos.get('detalle_orden'))

                productos = []
                for cantidad, descripcion, precio_unitario in zip(cantidades, descripciones, precios_unitarios):
                    productos.append({
                        'cantidad': cantidad,
                        'descripcion': descripcion.strip(),
                        'precio_unitario': precio_unitario
                    })

                    print(productos)

                return render(request, self.template_name, {
                    'pdf_form': PDFUploadForm(),  # Volver a mostrar el formulario vacío
                    'oc_form': oc_form,
                    'productos': productos, #ESTO LO AGREGUE AHORA
                })
            else:
                return render(request, self.template_name, {
                    'pdf_form': pdf_form,
                    'oc_form': nuevaOCForm()
                })
        # Si se está enviando el formulario de la orden de compra
        else:
            oc_form = nuevaOCForm(request.POST)
            if oc_form.is_valid():
                # oc_form.save() abajo de esto lo agregue ahora
                orden_compra = oc_form.save()
                # Guardar los productos asociados a la orden de compra
                for i in range(len(request.POST.getlist('productos[0][cantidad]'))):
                    Producto.objects.create(
                        orden_compra=orden_compra,
                        cantidad=request.POST.getlist(f'productos[{i}][cantidad]')[0],
                        descripcion=request.POST.getlist(f'productos[{i}][descripcion]')[0],
                        precio_unitario=request.POST.getlist(f'productos[{i}][precio_unitario]')[0]
                    )
                return redirect('oc:listado_oc')  # Redirige a la página de listado
            else:
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


#CARGAR PDF///////////////////////////////////////////////////////////
# class PDFUploadView(View):
#     def get(self, request):
#         form = PDFUploadForm()
#         return render(request, 'subir_pdf.html', {'form': form})

#     def post(self, request):
#         form = PDFUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             pdf_instance = form.save()
#             datos = extraer_datos(pdf_instance.file.path)  # Extrae los datos del PDF
            
#             # Imprimir los datos extraídos para verificar
#             print(datos)

#             cliente = Cliente.objects.get(cliente=datos.get('uoc'))
            
#             # Configura los datos extraídos como valores iniciales en el formulario
#             oc_form = nuevaOCForm(initial={
#                 'numero': datos.get('numero_orden') or '',
#                 'fecha': datos.get('fecha_orden') or '',
#                 'nrocompulsa': datos.get('numero_compulsa') or '',
#                 'afiliado': datos.get('nombre_afiliado') or '',
#                 'domicilioafiliado': "Dirección no especificada en el PDF", 
#                 'cliente': cliente.id or '',  # Guardar como afiliado si no se selecciona cliente
#                 'estado': 'pendiente',  # Puedes configurar un estado predeterminado
#                 'detalle': datos.get('detalle_orden') or '',
#                 'importe_total': datos.get('importe_total') or ''
#             })
#             return render(request, 'nueva_oc.html', {'form': oc_form})
#         return render(request, 'subir_pdf.html', {'form': form})