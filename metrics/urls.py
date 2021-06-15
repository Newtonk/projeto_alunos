from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('logout/', views.logoutUser, name="logout"),

    path('graphs_genero/', views.graphs_genero, name="graphs_genero"),
    path('graphs_social_class/', views.graphs_social_class, name="graphs_social_class"),
    path('graphs_sallary/', views.graphs_sallary, name="graphs_sallary"),
    path('update_graph/', views.update_graph, name="update_graph"),
    path('graphs_profissionais_vs_empresa/', views.graphs_profissionais_vs_empresa, name="graphs_profissionais_vs_empresa"),
    path('graphs_universidade_vs_empresa/', views.graphs_universidade_vs_empresa, name="graphs_universidade_vs_empresa"),
]