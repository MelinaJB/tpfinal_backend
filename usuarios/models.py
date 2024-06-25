from django.db import models

# Create your models here.

class tutorialesContenido(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    recurso_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.titulo


