from django.db import models
from django.contrib.auth.models import User

class TestResult(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    respuestas = models.JSONField()

    def __str__(self):
        return f"Test de {self.usuario.username} - {self.fecha.strftime('%d/%m/%Y')}"

class IkigaiResult(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    respuestas = models.JSONField()

    def __str__(self):
        return f"IKIGAI de {self.usuario.username} - {self.fecha.strftime('%d/%m/%Y')}"

class Carrera(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    area = models.CharField(max_length=50)  # Ej: salud, tecnología, social
    habilidades_clave = models.TextField()  # Separadas por coma

    def __str__(self):
        return self.nombre
    
class Mentor(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    descripcion = models.TextField()
    contacto = models.CharField(max_length=100, blank=True)  # NUEVO CAMPO
    carreras = models.ManyToManyField(Carrera)

    def __str__(self):
        return self.nombre
