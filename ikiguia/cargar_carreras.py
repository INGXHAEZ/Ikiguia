import os
import django

# Configura el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ikiguia.settings')  # ajusta si tu proyecto tiene otro nombre
django.setup()

from usuarios.models import Carrera

# Lista de carreras a insertar
carreras_data = [
    {
        "nombre": "Medicina",
        "descripcion": "La carrera de Medicina forma profesionales capaces de diagnosticar, tratar y prevenir enfermedades humanas, con un enfoque ético y científico. Requiere una alta vocación de servicio y compromiso social.",
        "area": "Ciencias de la Salud",
        "habilidades_clave": ["Anatomía", "Biología", "Comunicación empática", "Toma de decisiones", "Trabajo bajo presión"]
    },
    {
        "nombre": "Ingeniería en Sistemas",
        "descripcion": "Forma profesionales en el diseño, desarrollo y gestión de sistemas de software y hardware. Se enfoca en resolver problemas informáticos con soluciones innovadoras y eficientes.",
        "area": "Tecnología",
        "habilidades_clave": ["Programación", "Pensamiento lógico", "Algoritmos", "Resolución de problemas", "Análisis de sistemas"]
    },
    {
        "nombre": "Derecho",
        "descripcion": "El Derecho prepara expertos en leyes, justicia y normativas. Capacita a los estudiantes para interpretar y aplicar el marco legal de manera ética y justa.",
        "area": "Ciencias Jurídicas",
        "habilidades_clave": ["Análisis crítico", "Oratoria", "Interpretación de textos", "Resolución de conflictos", "Ética profesional"]
    },
    {
        "nombre": "Psicología",
        "descripcion": "La Psicología estudia el comportamiento humano y los procesos mentales. Los profesionales pueden trabajar en salud mental, recursos humanos o investigación.",
        "area": "Ciencias Sociales",
        "habilidades_clave": ["Escucha activa", "Empatía", "Observación", "Comunicación", "Evaluación psicológica"]
    },
    {
        "nombre": "Administración de Empresas",
        "descripcion": "Forma líderes capaces de dirigir organizaciones, gestionar recursos y tomar decisiones estratégicas en entornos competitivos y cambiantes.",
        "area": "Administración",
        "habilidades_clave": ["Liderazgo", "Toma de decisiones", "Planificación", "Finanzas", "Comunicación"]
    },
    {
        "nombre": "Arquitectura",
        "descripcion": "Forma profesionales capaces de diseñar y planificar espacios funcionales y estéticos, considerando factores técnicos, culturales y ambientales.",
        "area": "Tecnología",
        "habilidades_clave": ["Diseño", "Creatividad", "Dibujo técnico", "Pensamiento espacial", "Trabajo en equipo"]
    },
    {
        "nombre": "Ingeniería Civil",
        "descripcion": "Prepara profesionales para diseñar, construir y mantener infraestructuras como puentes, carreteras y edificios, aplicando principios científicos y técnicos.",
        "area": "Tecnología",
        "habilidades_clave": ["Matemáticas", "Diseño estructural", "Resolución de problemas", "Gestión de proyectos", "Trabajo en equipo"]
    },
    {
        "nombre": "Ingeniería Industrial",
        "descripcion": "Forma expertos en la optimización de procesos productivos y administrativos, buscando eficiencia en recursos humanos, materiales y tecnológicos.",
        "area": "Tecnología",
        "habilidades_clave": ["Gestión de procesos", "Análisis de datos", "Optimización", "Planificación", "Productividad"]
    },
    {
        "nombre": "Contabilidad y Auditoría",
        "descripcion": "Prepara profesionales en el manejo de información financiera, contable y fiscal, esenciales para la toma de decisiones en organizaciones públicas y privadas.",
        "area": "Finanzas",
        "habilidades_clave": ["Contabilidad", "Análisis financiero", "Precisión", "Ética", "Normas fiscales"]
    },
    {
        "nombre": "Pedagogía en Educación Básica",
        "descripcion": "Capacita a docentes para formar integralmente a niños y niñas en sus primeras etapas escolares, fomentando el aprendizaje activo y la formación de valores.",
        "area": "Educación",
        "habilidades_clave": ["Didáctica", "Paciencia", "Comunicación", "Creatividad", "Planificación educativa"]
    },
    {
        "nombre": "Periodismo",
        "descripcion": "Forma comunicadores capaces de investigar, redactar y difundir información veraz a través de medios escritos, radiales, televisivos o digitales.",
        "area": "Comunicación",
        "habilidades_clave": ["Redacción", "Investigación", "Objetividad", "Edición", "Manejo de medios"]
    },
    {
        "nombre": "Enfermería",
        "descripcion": "Prepara profesionales que brindan cuidados integrales a pacientes, promoviendo la salud, previniendo enfermedades y asistiendo en tratamientos médicos.",
        "area": "Ciencias de la Salud",
        "habilidades_clave": ["Atención al paciente", "Trabajo en equipo", "Empatía", "Gestión del tiempo", "Conocimiento clínico"]
    },
    {
        "nombre": "Diseño Gráfico",
        "descripcion": "Forma creativos capaces de comunicar mensajes visuales de manera efectiva a través de herramientas gráficas digitales y tradicionales.",
        "area": "Arte y Diseño",
        "habilidades_clave": ["Diseño", "Creatividad", "Adobe Illustrator", "Comunicación visual", "Edición digital"]
    },
    {
        "nombre": "Gastronomía",
        "descripcion": "Capacita a los estudiantes en técnicas culinarias, gestión de cocina y cultura gastronómica, con enfoque en creatividad, nutrición y presentación.",
        "area": "Turismo y Hospitalidad",
        "habilidades_clave": ["Cocina", "Creatividad", "Higiene", "Trabajo bajo presión", "Organización"]
    },
    {
        "nombre": "Biología",
        "descripcion": "Estudia los seres vivos desde un enfoque científico, preparando profesionales para la investigación, docencia y conservación del medio ambiente.",
        "area": "Ciencias Naturales",
        "habilidades_clave": ["Observación", "Investigación", "Análisis", "Conocimiento científico", "Curiosidad"]
    },
    {
        "nombre": "Marketing",
        "descripcion": "Forma profesionales en el análisis del mercado, diseño de estrategias comerciales y promoción de productos o servicios para alcanzar los objetivos de la empresa.",
        "area": "Administración",
        "habilidades_clave": ["Comunicación", "Creatividad", "Análisis de mercado", "Negociación", "Publicidad"]
    },
    {
        "nombre": "Ingeniería Mecánica",
        "descripcion": "Capacita a los estudiantes para diseñar, fabricar y mantener sistemas mecánicos e industriales con enfoque en innovación y eficiencia.",
        "area": "Tecnología",
        "habilidades_clave": ["Diseño mecánico", "Matemáticas", "Resolución de problemas", "Tecnología", "Precisión"]
    },
    {
        "nombre": "Ingeniería Electrónica",
        "descripcion": "Forma expertos en el diseño y desarrollo de sistemas electrónicos, automatización y control, con impacto en diversos sectores tecnológicos.",
        "area": "Tecnología",
        "habilidades_clave": ["Circuitos", "Electrónica", "Lógica digital", "Programación", "Innovación"]
    },
    {
        "nombre": "Trabajo Social",
        "descripcion": "Prepara profesionales comprometidos con la mejora de la calidad de vida de personas y comunidades en situación de vulnerabilidad.",
        "area": "Ciencias Sociales",
        "habilidades_clave": ["Empatía", "Comunicación", "Gestión social", "Análisis de casos", "Servicio comunitario"]
    },
    {
        "nombre": "Nutrición y Dietética",
        "descripcion": "Capacita a profesionales en alimentación saludable, valoración nutricional y prevención de enfermedades relacionadas con la dieta.",
        "area": "Ciencias de la Salud",
        "habilidades_clave": ["Nutrición", "Educación alimentaria", "Análisis clínico", "Empatía", "Planificación de dietas"]
    },
    {
        "nombre": "Educación Física",
        "descripcion": "Forma docentes que promueven la actividad física, el deporte y la salud integral en diversos contextos educativos y recreativos.",
        "area": "Educación",
        "habilidades_clave": ["Deporte", "Motivación", "Planificación", "Psicomotricidad", "Liderazgo"]
    },
    {
        "nombre": "Turismo",
        "descripcion": "Prepara a los estudiantes para gestionar actividades turísticas, culturales y recreativas con enfoque en sostenibilidad y servicio al cliente.",
        "area": "Turismo y Hospitalidad",
        "habilidades_clave": ["Atención al cliente", "Idiomas", "Gestión turística", "Organización", "Relaciones públicas"]
    },
    {
        "nombre": "Ciencias Ambientales",
        "descripcion": "Estudia las relaciones entre los seres vivos y su entorno para proponer soluciones sostenibles a los problemas ambientales actuales.",
        "area": "Ciencias Naturales",
        "habilidades_clave": ["Ecología", "Investigación", "Educación ambiental", "Trabajo en campo", "Conciencia ecológica"]
    }
]

# Inserta las carreras en la base de datos
for data in carreras_data:
    carrera, created = Carrera.objects.get_or_create(
        nombre=data["nombre"],
        defaults={
            "descripcion": data["descripcion"],
            "area": data["area"],
            "habilidades_clave": data["habilidades_clave"]
        }
    )
    if created:
        print(f"✅ Carrera creada: {carrera.nombre}")
    else:
        print(f"ℹ️ Carrera ya existente: {carrera.nombre}")
