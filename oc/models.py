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
    nrocompulsa = models.CharField(max_length=20,default='0000-0000', blank=True, null=True)
    afiliado = models.CharField(max_length=200, blank=True, null=True)
    domicilioafiliado = models.CharField(max_length=300, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    importe_total = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    entrega_unica = models.BooleanField(default=True)

    
    def __str__(self):
        return self.numero + ' - ' + self.estado  # Puedes cambiar esto según cómo quieras mostrar la orden de compra en el admin

class Producto(models.Model):
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='productos')
    cantidad = models.IntegerField()
    descripcion = models.CharField(max_length=255, default="")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.descripcion} - {self.orden_compra.numero}'
    

#SUBIR PDF ////////////////
# class PDFDocument(models.Model):
    # file = models.FileField(upload_to='pdfs/')
    # extracted_data = models.TextField(blank=True, null=True)  # Puedes ajustar el tipo de campo según la información
    # uploaded_at = models.DateTimeField(auto_now_add=True)

class PDFDocument(models.Model):
    # orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='pdfs', default=1)  # Asumiendo que 1 es un ID válido de OrdenCompra
    file = models.FileField(upload_to='pdfs/')
    extracted_data = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.orden_compra.numero} - PDF'
