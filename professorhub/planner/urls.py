from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('disciplinas/', views.disciplinas, name='disciplinas'),
    path('tarefas/', views.tarefas, name='tarefas'),
]