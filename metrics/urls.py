from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),

    path('dashboard_profissionais/', views.dashboard_profissionais, name="dashboard_profissionais"),
]