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
    area = models.CharField(max_length=50)
    habilidades_clave = models.JSONField()  

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

class Mentoria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mentor = models.ForeignKey('Mentor', on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    mensaje = models.TextField(blank=True)
    confirmada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario.username} con {self.mentor.nombre} el {self.fecha} a las {self.hora}"