from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),

    path('graphs_profissionais_vs_universidade/', views.graphs_profissionais_vs_universidade, name="graphs_profissionais_vs_universidade"),
    path('update_graph/', views.update_graph, name="update_graph"),
    path('graphs_profissionais_vs_empresa/', views.graphs_profissionais_vs_empresa, name="graphs_profissionais_vs_empresa"),
    path('graphs_universidade_vs_empresa/', views.graphs_universidade_vs_empresa, name="graphs_universidade_vs_empresa"),
]