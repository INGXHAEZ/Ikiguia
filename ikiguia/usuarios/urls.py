from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('test/', views.test_psicometrico, name='test'),
    path('test-ikigai/', views.test_ikigai, name='test_ikigai'),
    path('carreras/', views.carreras_recomendadas, name='carreras'),
    path('mentores/', views.mentores_recomendados, name='mentores'),
    path('agendar-mentoria/', views.agendar_mentoria, name='agendar_mentoria'),
    path('perfil-vocacional/', views.perfil_vocacional, name='perfil_vocacional'),
    path('perfil_vocacional/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil-vocacional/pdf/', views.descargar_perfil_pdf, name='descargar_perfil'),
    path('politica-de-datos/', views.politica_proteccion_datos, name='politica_datos'),
    path('politica-privacidad/', views.politica_privacidad, name='politica_privacidad'),
]
