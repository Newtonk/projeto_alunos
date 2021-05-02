from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),

    path('dashboard_perfil_aluno/', views.dashboard_perfil_aluno, name="dashboard_perfil_aluno"),
    path('dashboard_areas_atuacao/', views.dashboard_areas_atuacao, name="dashboard_areas_atuacao"),
]