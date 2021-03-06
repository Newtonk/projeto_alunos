from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('logout/', views.logoutUser, name="logout"),

    path('graphs_genero/', views.graphs_genero, name="graphs_genero"),
    path('graphs_social_class/', views.graphs_social_class, name="graphs_social_class"),
    path('graphs_sallary/', views.graphs_sallary, name="graphs_sallary"),
    path('graphs_age/', views.graphs_age, name="graphs_age"),
    path('graphs_quantity/', views.graphs_quantity, name="graphs_quantity"),
    path('update_graph/', views.update_graph, name="update_graph"),
]