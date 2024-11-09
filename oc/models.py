from django.db import models

# Create your models here.

class Cliente(models.Model):
    cliente = models.CharField(max_length=200, unique=True)
    cuit = models.CharField(max_length=13)
    domiciliocliente = models.CharField(max_length=200)

    def __str__(self):
        return self.cliente

class OrdenCompra(models.Model):
    ESTADO_CHOICES = [
        ('certificado', 'Certificado'),
        ('baja', 'Baja'),
        ('entregada', 'Entregada'),
        ('pendiente', 'Pendiente'),
        ('activa', 'Activa'),
    ]

    numero = models.CharField(max_length=20, default='4500', unique=True)
    fecha = models.DateField(blank=True, null=True)
    nrocompulsa = models.CharField(max_length=20,default='4500', blank=True, null=True)
    afiliado = models.CharField(max_length=200, blank=True, null=True)
    domicilioafiliado = models.CharField(max_length=300, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    entrega_unica = models.BooleanField(default=True)

    def __str__(self):
        return self.numero + ' - ' + self.estado  # Puedes cambiar esto según cómo quieras mostrar la orden de compra en el admin

class Producto(models.Model):
    orden_compra = models.ForeignKey(OrdenCompra, related_name='productos', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    detalle = models.CharField(max_length=200)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.detalle} - {self.orden_compra.numero}'

#SUBIR PDF ////////////////
class PDFDocument(models.Model):
    file = models.FileField(upload_to='pdfs/')
    extracted_data = models.TextField(blank=True, null=True)  # Puedes ajustar el tipo de campo según la información
    uploaded_at = models.DateTimeField(auto_now_add=True)

