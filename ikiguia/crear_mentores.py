import os
import django

# Configura el entorno Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ikiguia.settings")
django.setup()

from usuarios.models import Mentor
from carreras.models import Carrera  # Ajusta si el modelo está en otro lugar

mentores = [
    {
        "nombre": "Dra. Valeria Medina",
        "especialidad": "Neurología",
        "descripcion": "Médica especialista en neurología con 12 años de experiencia...",
        "contacto": "valeria.medina@ikiguia.com",
        "carreras": ["Medicina", "Enfermería"]
    },
    {
        "nombre": "Ing. Carlos Andrade",
        "especialidad": "Ingeniería de Software",
        "descripcion": "Desarrollador senior en una multinacional de tecnología...",
        "contacto": "carlos.andrade@ikiguia.com",
        "carreras": ["Ingeniería en Sistemas", "Ingeniería Electrónica"]
    },
    {
        "nombre": "Lic. Mariana Torres",
        "especialidad": "Psicología Educativa",
        "descripcion": "Psicóloga con enfoque en el desarrollo infantil...",
        "contacto": "mariana.torres@ikiguia.com",
        "carreras": ["Psicología", "Pedagogía en Educación Básica"]
    },
    {
        "nombre": "Dr. Andrés Pérez",
        "especialidad": "Derecho Penal",
        "descripcion": "Abogado litigante con experiencia en causas penales...",
        "contacto": "andres.perez@ikiguia.com",
        "carreras": ["Derecho"]
    },
    {
        "nombre": "MSc. Sofía Aguilar",
        "especialidad": "Gestión Empresarial",
        "descripcion": "Consultora estratégica en negocios con enfoque en liderazgo femenino...",
        "contacto": "sofia.aguilar@ikiguia.com",
        "carreras": ["Administración de Empresas", "Marketing"]
    },
    {
        "nombre": "Arq. Diego Vélez",
        "especialidad": "Diseño Arquitectónico",
        "descripcion": "Arquitecto con más de 15 años de experiencia en proyectos urbanos sostenibles...",
        "contacto": "diego.velez@ikiguia.com",
        "carreras": ["Arquitectura"]
    },
    {
        "nombre": "Ing. Paulina Cueva",
        "especialidad": "Ingeniería Estructural",
        "descripcion": "Experta en diseño de estructuras resistentes a sismos...",
        "contacto": "paulina.cueva@ikiguia.com",
        "carreras": ["Ingeniería Civil"]
    },
    {
        "nombre": "Ing. David Romero",
        "especialidad": "Procesos Industriales",
        "descripcion": "Ingeniero industrial con experiencia en mejora continua...",
        "contacto": "david.romero@ikiguia.com",
        "carreras": ["Ingeniería Industrial"]
    },
    {
        "nombre": "Lcda. Julia León",
        "especialidad": "Auditoría Financiera",
        "descripcion": "Contadora pública certificada. Se ha desempeñado como auditora en firmas internacionales...",
        "contacto": "julia.leon@ikiguia.com",
        "carreras": ["Contabilidad y Auditoría"]
    },
    {
        "nombre": "Prof. Guillermo Álvarez",
        "especialidad": "Educación Básica",
        "descripcion": "Docente con 25 años de experiencia en aula. Creador de materiales didácticos...",
        "contacto": "guillermo.alvarez@ikiguia.com",
        "carreras": ["Pedagogía en Educación Básica"]
    },
    # Puedes continuar con los otros mentores si deseas
]

for data in mentores:
    mentor, created = Mentor.objects.get_or_create(
        nombre=data["nombre"],
        defaults={
            "especialidad": data["especialidad"],
            "descripcion": data["descripcion"],
            "contacto": data["contacto"]
        }
    )
    for carrera_nombre in data["carreras"]:
        carrera = Carrera.objects.filter(nombre=carrera_nombre).first()
        if carrera:
            mentor.carreras.add(carrera)
        else:
            print(f"⚠️ Carrera no encontrada: {carrera_nombre}")
    mentor.save()

print("✅ Mentores cargados exitosamente.")
