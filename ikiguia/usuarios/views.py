from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import TestForm
from .models import TestResult
from django.shortcuts import render
from .models import TestResult
from .forms import IkigaiForm
from .models import IkigaiResult
from .models import Carrera
from django.db.models import Q
from .models import Mentor
from .forms import MentoriaForm
from .models import Mentoria
from django.contrib import messages
from .forms import UserProfileForm
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse

def calcular_afinidad(ikigai, carrera):
    pesos = {
        'ama': 3,
        'bueno': 2,
        'pagado': 2,
        'necesario': 1
    }

    afinidad = 0
    peso_total = 0

    habilidades = carrera.habilidades_clave.lower().split(",")
    habilidades = [h.strip() for h in habilidades]

    for categoria, peso in pesos.items():
        claves = ikigai.get(categoria, [])
        for palabra in claves:
            for habilidad in habilidades:
                if palabra.strip().lower() in habilidad:
                    afinidad += peso
        peso_total += peso * len(claves)

    return round((afinidad / peso_total) * 100) if peso_total > 0 else 0

def home(request):
    return render(request, 'home.html')

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def cerrar_sesion(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    resultado = TestResult.objects.filter(usuario=request.user).last()
    ikigai_result = IkigaiResult.objects.filter(usuario=request.user).last()
    mentorias = Mentoria.objects.filter(usuario=request.user)

    analisis = None
    if resultado:
        respuestas = resultado.respuestas
        promedio = sum(int(v) for v in respuestas.values()) / len(respuestas)
        if promedio >= 4.5:
            analisis = "Tienes un perfil altamente enfocado, con gran claridad en tus intereses y fortalezas."
        elif promedio >= 3.5:
            analisis = "Tu perfil muestra una buena base de intereses. Con algo de orientación, podrías identificar claramente tu vocación."
        elif promedio >= 2.5:
            analisis = "Hay señales de indecisión o áreas mixtas. Sería útil que explores más opciones o tomes otro test complementario."
        else:
            analisis = "Parece que necesitas mayor reflexión sobre tus intereses. Prueba el test IKIGAI para profundizar en tu propósito."

    # Procesar resultado IKIGAI
    ikigai = {}
    carreras_afines = []
    mentores = []

    if ikigai_result:
        datos = ikigai_result.respuestas
        ikigai = {
            'ama': [datos.get('ama_1', ''), datos.get('ama_2', '')],
            'bueno': [datos.get('bueno_1', ''), datos.get('bueno_2', '')],
            'pagado': [datos.get('pagado_1', ''), datos.get('pagado_2', '')],
            'necesario': [datos.get('necesario_1', ''), datos.get('necesario_2', '')],
        }

        # 🔍 Recomendaciones de carrera basadas en palabras clave IKIGAI
        palabras_clave = list(datos.values())
        query = Q()
        for palabra in palabras_clave:
            query |= Q(habilidades_clave__icontains=palabra)

        carreras = Carrera.objects.filter(query).distinct()

        for carrera in carreras:
            afinidad = calcular_afinidad(ikigai, carrera)
            carreras_afines.append((carrera, afinidad))

        carreras_afines.sort(key=lambda x: x[1], reverse=True)

        mentores = Mentor.objects.filter(carreras__in=carreras).distinct()

    return render(request, 'dashboard.html', {
        'resultado': resultado,
        'analisis': analisis,
        'ikigai': ikigai,
        'mentorias': mentorias,
        'carreras': carreras_afines,
        'mentores': mentores,
    })


@login_required
def test_psicometrico(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            respuestas = form.cleaned_data
            TestResult.objects.create(usuario=request.user, respuestas=respuestas)
            return redirect('dashboard')
    else:
        form = TestForm()
    return render(request, 'test.html', {'form': form})

@login_required
def test_ikigai(request):
    if request.method == 'POST':
        form = IkigaiForm(request.POST)
        if form.is_valid():
            respuestas = form.cleaned_data
            IkigaiResult.objects.create(usuario=request.user, respuestas=respuestas)
            return redirect('dashboard')
    else:
        form = IkigaiForm()
    return render(request, 'ikigai.html', {'form': form})

@login_required
def carreras_recomendadas(request):
    ikigai_result = IkigaiResult.objects.filter(usuario=request.user).last()
    carreras = []

    if ikigai_result:
        respuestas = ikigai_result.respuestas
        palabras_clave = list(respuestas.values())
        print("Palabras clave del IKIGAI:", palabras_clave)  # <-- Añade esto

        query = Q()
        for palabra in palabras_clave:
            query |= Q(habilidades_clave__icontains=palabra)

        carreras = Carrera.objects.filter(query).distinct()

    return render(request, 'carreras.html', {'carreras': carreras})

@login_required
def mentores_recomendados(request):
    ikigai_result = IkigaiResult.objects.filter(usuario=request.user).last()
    mentores_afines = []

    if ikigai_result:
        respuestas = ikigai_result.respuestas
        ikigai = {
            'ama': [respuestas.get('ama_1', ''), respuestas.get('ama_2', '')],
            'bueno': [respuestas.get('bueno_1', ''), respuestas.get('bueno_2', '')],
            'pagado': [respuestas.get('pagado_1', ''), respuestas.get('pagado_2', '')],
            'necesario': [respuestas.get('necesario_1', ''), respuestas.get('necesario_2', '')],
        }

        carreras = Carrera.objects.all()

        for carrera in carreras:
            afinidad = calcular_afinidad(ikigai, carrera)
            if afinidad >= 50:  # solo considera si hay al menos 50% de coincidencia
                for mentor in carrera.mentor_set.all():
                    mentores_afines.append((mentor, afinidad))

        mentores_afines = list(set(mentores_afines))  # eliminar duplicados
        mentores_afines.sort(key=lambda x: x[1], reverse=True)

    return render(request, 'mentores.html', {'mentores': mentores_afines})

@login_required
def agendar_mentoria(request):
    if request.method == 'POST':
        form = MentoriaForm(request.POST, initial={'usuario': request.user})
        if form.is_valid():
            mentoria = form.save(commit=False)
            mentoria.usuario = request.user
            mentoria.save()
            messages.success(request, '✅ ¡Mentoría agendada exitosamente!')
            return redirect('dashboard')
        else:
             messages.error(request, '⚠️ No se pudo agendar, dia y hora ocupados')
    else:
        form = MentoriaForm(initial={'usuario': request.user})
    return render(request, 'agendar_mentoria.html', {'form': form})

@login_required
def editar_perfil(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('perfil')  
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'editar_perfil.html', {'form': form})

@login_required
def perfil_usuario(request):
    return render(request, 'perfil_vocacional.html', {'usuario': request.user})

@login_required
def perfil_vocacional(request):
    user = request.user
    test_result = TestResult.objects.filter(usuario=user).last()
    ikigai_result = IkigaiResult.objects.filter(usuario=user).last()
    carreras_afines = []

    fortalezas = []
    ikigai = {}

    if test_result:
        respuestas = test_result.respuestas
        fortalezas = [
            ("Trabajo en equipo", respuestas.get("pregunta1", 0)),
            ("Resolución de problemas", respuestas.get("pregunta2", 0)),
            ("Tareas prácticas", respuestas.get("pregunta3", 0)),
            ("Interés científico", respuestas.get("pregunta4", 0)),
            ("Ayuda a los demás", respuestas.get("pregunta5", 0)),
        ]
        fortalezas.sort(key=lambda x: int(x[1]), reverse=True)

    if ikigai_result:
        datos = ikigai_result.respuestas
        ikigai_claves = list(datos.values())
        ikigai = {
            'ama': [datos.get('ama_1', ''), datos.get('ama_2', '')],
            'bueno': [datos.get('bueno_1', ''), datos.get('bueno_2', '')],
            'pagado': [datos.get('pagado_1', ''), datos.get('pagado_2', '')],
            'necesario': [datos.get('necesario_1', ''), datos.get('necesario_2', '')],
        }

        query = Q()
        for palabra in ikigai_claves:
            query |= Q(habilidades_clave__icontains=palabra)

        carreras = Carrera.objects.filter(query).distinct()

        for carrera in carreras:
            afinidad = calcular_afinidad(ikigai, carrera)
            carreras_afines.append((carrera, afinidad))


        carreras_afines.sort(key=lambda x: x[1], reverse=True)

    return render(request, 'perfil_vocacional.html', {
        'fortalezas': fortalezas,
        'ikigai': ikigai,
        'carreras_afines': carreras_afines,
        'usuario': request.user
    })


@login_required
def descargar_perfil_pdf(request):
    user = request.user
    test_result = TestResult.objects.filter(usuario=user).last()
    ikigai_result = IkigaiResult.objects.filter(usuario=user).last()

    fortalezas = []
    carreras_afines = []

    if test_result:
        respuestas = test_result.respuestas
        fortalezas = [
            ("Trabajo en equipo", respuestas.get("pregunta1", 0)),
            ("Resolución de problemas", respuestas.get("pregunta2", 0)),
            ("Tareas prácticas", respuestas.get("pregunta3", 0)),
            ("Interés científico", respuestas.get("pregunta4", 0)),
            ("Ayuda a los demás", respuestas.get("pregunta5", 0)),
        ]
        fortalezas.sort(key=lambda x: int(x[1]), reverse=True)

    ikigai = {}
    if ikigai_result:
        datos = ikigai_result.respuestas
        ikigai = {
            'ama': [datos.get('ama_1', ''), datos.get('ama_2', '')],
            'bueno': [datos.get('bueno_1', ''), datos.get('bueno_2', '')],
            'pagado': [datos.get('pagado_1', ''), datos.get('pagado_2', '')],
            'necesario': [datos.get('necesario_1', ''), datos.get('necesario_2', '')],
        }

        palabras_clave = list(datos.values())
        query = Q()
        for palabra in palabras_clave:
            query |= Q(habilidades_clave__icontains=palabra)

        carreras = Carrera.objects.filter(query).distinct()

        for carrera in carreras:
            afinidad = calcular_afinidad(ikigai, carrera)
            carreras_afines.append((carrera, afinidad))

        carreras_afines.sort(key=lambda x: x[1], reverse=True)

    # Renderizar el PDF
    template = get_template('perfil_vocacional_pdf.html')
    html = template.render({
        'usuario': user,
        'fortalezas': fortalezas,
        'ikigai': ikigai,
        'carreras_afines': carreras_afines
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="perfil_vocacional.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response