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

    # Procesar el resultado IKIGAI si existe
    ikigai = {}
    if ikigai_result:
        datos = ikigai_result.respuestas
        ikigai = {
            'ama': [datos.get('ama_1', ''), datos.get('ama_2', '')],
            'bueno': [datos.get('bueno_1', ''), datos.get('bueno_2', '')],
            'pagado': [datos.get('pagado_1', ''), datos.get('pagado_2', '')],
            'necesario': [datos.get('necesario_1', ''), datos.get('necesario_2', '')],
        }

    return render(request, 'dashboard.html', {
        'resultado': resultado,
        'analisis': analisis,
        'ikigai': ikigai
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
    mentores = []

    if ikigai_result:
        respuestas = ikigai_result.respuestas
        palabras_clave = list(respuestas.values())
        
        # Buscar carreras relacionadas
        query = Q()
        for palabra in palabras_clave:
            query |= Q(habilidades_clave__icontains=palabra)

        carreras = Carrera.objects.filter(query).distinct()

        # Obtener mentores que estén relacionados con esas carreras
        mentores = Mentor.objects.filter(carreras__in=carreras).distinct()

    return render(request, 'mentores.html', {'mentores': mentores})