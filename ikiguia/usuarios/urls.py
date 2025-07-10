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
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
]
