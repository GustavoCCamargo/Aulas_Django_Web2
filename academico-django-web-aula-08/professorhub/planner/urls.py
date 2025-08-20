from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('disciplinas/', views.disciplinas, name='disciplinas'),

    path('tarefas/', views.tarefas, name='tarefas'),

    #UC - Gerir calendário letivo
    path('calendarios/', views.listar_calendarios, name='listar_calendarios'), #lista todos os calendarios letivos
    path('calendario/adicionar/', views.adicionar_calendario, name='adicionar_calendario'), #tela de adicionar calendario letivo
    path('calendario/cadastrar/', views.cadastrar_calendario, name='cadastrar_calendario'), #view que processa o cadastro de um calendario letivo

    #remove um calendario letivo que tenha um id especifico
    path('calendario/remover/<int:id>/', views.remover_calendario, name='remover_calendario'),
    
    #edita um calendario letivo que tenha um id especifico
    path('calendario/editar/<int:id>/', views.editar_calendario, name='editar_calendario'), #tela de editar calendario letivo
    path('calendario/atualizar/<int:id>/', views.atualizar_calendario, name='atualizar_calendario'), #view que processa a atualizacao de um calendario letivo

    #UC - Gerir disciplinas
    path('disciplinas/listar/', views.listar_disciplinas, name='listar_disciplinas'),
    path('disciplina/adicionar/', views.adicionar_disciplina, name='adicionar_disciplina'),
    path('disciplina/cadastrar/', views.cadastrar_disciplina, name='cadastrar_disciplina'),
    path('disciplina/remover/<int:id>/', views.remover_disciplina, name='remover_disciplina'),
    path('disciplina/<int:id>/editar/', views.editar_disciplina, name='editar_disciplina'),
    path('disciplina/<int:id>/atualizar/', views.atualizar_disciplina, name='atualizar_disciplina'),

    #UC - Gerir planos de aula
    path('disciplina/<int:disciplina_id>/planos/', views.listar_planos_aula, name='listar_planos_aula'),
    path('disciplina/<int:disciplina_id>/plano/adicionar/', views.adicionar_plano_aula, name='adicionar_plano_aula'),
    path('disciplina/<int:disciplina_id>/plano/cadastrar/', views.cadastrar_plano_aula, name='cadastrar_plano_aula'),
    path('disciplina/<int:disciplina_id>/plano/<int:plano_id>/editar/', views.editar_plano_aula, name='editar_plano_aula'),
    path('disciplina/<int:disciplina_id>/plano/<int:plano_id>/atualizar/', views.atualizar_plano_aula, name='atualizar_plano_aula'),    
    path('disciplina/<int:disciplina_id>/plano/<int:plano_id>/remover/', views.remover_plano_aula, name='remover_plano_aula'),
]