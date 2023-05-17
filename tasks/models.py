from django.db import models

class Task(models.Model):
    imagen = models.ImageField(upload_to='images/', blank=True, null=True)
    texto_generado = models.CharField(max_length=200, blank=True, null=True)
    texto_ingresado = models.CharField(max_length=200, blank=True, null=True)
    precision = models.IntegerField(default=0)

    def __str__(self):
        return f"Placa ID: {self.id}"
