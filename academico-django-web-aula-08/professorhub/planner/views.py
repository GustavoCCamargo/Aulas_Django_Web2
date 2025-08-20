
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from .models import CalendarioLetivo, DataImportante, Disciplina, PlanoAula
from .forms import CalendarioLetivoForm, DisciplinaForm, PlanoAulaForm

@login_required(login_url='index')  # nome da rota para onde redireciona se não estiver logado
def admin_dashboard(request):
    return render(request, 'planner/admin_dashboard.html')


@login_required(login_url='index') 
def disciplinas(request):
    # Redireciona para a nova view de listagem de disciplinas
    return redirect('listar_disciplinas')

@login_required
def listar_disciplinas(request):
    # Busca todas as disciplinas do usuário logado
    disciplinas_usuario = Disciplina.objects.filter(user=request.user)
    return render(request, 'planner/disciplina/listar.html', {
        'disciplinas': disciplinas_usuario
    })

@login_required
def adicionar_disciplina(request):
    # Cria um formulário vazio, passando o usuário logado para filtrar os calendários
    form = DisciplinaForm(user=request.user)
    return render(request, 'planner/disciplina/adicionar.html', {
        'form': form
    })

@login_required
@transaction.atomic
def cadastrar_disciplina(request):
    if request.method == 'POST':

        # Cria um formulário com os dados do POST
        # Este parâmetro não está sendo usado para definir o campo user do modelo. 
        # Em vez disso, ele está sendo usado para filtrar os calendários disponíveis no dropdown
        form = DisciplinaForm(request.POST, user=request.user)
        
        if form.is_valid():
            # Salva a disciplina, mas não comita ainda
            disciplina = form.save(commit=False)
            disciplina.user = request.user  # Associa ao usuário logado
            disciplina.save()  # Agora salva no banco de dados
            
            messages.success(request, 'Disciplina cadastrada com sucesso!')
            return redirect('listar_disciplinas')
        else:
            messages.error(request, 'Erro ao cadastrar disciplina.')
            return render(request, 'planner/disciplina/adicionar.html', {
                'form': form
            })
    else:
        return redirect('adicionar_disciplina')

@login_required
@transaction.atomic
def remover_disciplina(request, id):
    # Busca a disciplina pelo id e usuário logado
    disciplina = get_object_or_404(Disciplina, id=id, user=request.user)
    
    if request.method == 'POST':
        # Remove a disciplina
        disciplina.delete()
        messages.success(request, 'Disciplina removida com sucesso!')
        return redirect('listar_disciplinas')

@login_required
def editar_disciplina(request, id):
    # Busca a disciplina pelo id e usuário logado
    db_disciplina = get_object_or_404(Disciplina, id=id, user=request.user)

    #instancia os forms com os dados do banco de dados
    form = DisciplinaForm(instance=db_disciplina, user=request.user)

    return render(request, 'planner/disciplina/editar.html', {
        'form': form,
        'disciplina': db_disciplina
    })

'''
Metodo que processo o formulario que atualiza dados da disciplina
@param request: O objeto de requisição HTTP
@param id: O ID da disciplina a ser atualizada
'''
@login_required
def atualizar_disciplina(request, id):
    # Busca a disciplina pelo id e usuário logado
    db_disciplina = get_object_or_404(Disciplina, id=id, user=request.user)

    #processa o formulario
    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=db_disciplina, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('listar_disciplinas')
    else:
        form = DisciplinaForm(instance=db_disciplina, user=request.user)

    return render(request, 'planner/disciplina/editar.html', {
        'form': form,
        'disciplina': db_disciplina
    })

@login_required(login_url='index') 
def tarefas(request):
    return render(request, 'planner/tarefas.html')





# UC - Gerir calendário letivo
# Busca todos os calendarios do usuario logado e passa para o template.
# o metodo render renderiza o template 'listar.html' e passa o contexto com a lista de calendarios.
# no template, a lista de calendarios é acessada através da variável 'calendarios'.
@login_required
def listar_calendarios(request):
    calendarios_usuario_logado = CalendarioLetivo.objects.filter(user=request.user)
    return render(request, 'planner/calendario/listar.html', {
        'calendarios': calendarios_usuario_logado
    })

# UC - Gerir calendário letivo
# Cria um novo calendario letivo.
# O formulario CalendarioLetivoForm é instanciado e passado para o template 'adicionar.html'.
# O template renderiza o formulario para o usuario preencher.
# O metodo render renderiza o template 'adicionar.html' e passa o contexto com o formulario.
# no template, o formulario é acessado através da variável 'form'.
@login_required
def adicionar_calendario(request):
    form = CalendarioLetivoForm()
    return render(request, 'planner/calendario/adicionar.html', {
        'form': form
    })


# UC - Gerir calendário letivo
# Cadastra um novo calendario letivo.
# Este metodo é chamado quando o usuario envia o formulario do template 'adicionar.html'.
@login_required
@transaction.atomic # Garante que todas as operações de banco de dados sejam atômicas
def cadastrar_calendario(request):
    if request.method == 'POST':

        # O formulario CalendarioLetivoForm é instanciado com os dados do request.POST.
        form = CalendarioLetivoForm(request.POST)
        
        # Se o formulario for valido, o calendario é salvo no banco de dados.
        # is_valid() verifica se os dados do formulario estão corretos conforme o modelo CalendarioLetivo.
        if form.is_valid():
            #form.save(commit=False) cria uma instância do modelo CalendarioLetivo sem salvar no banco de dados ainda.
            # Isso permite que você adicione campos adicionais antes de salvar.
            # se quer salvar o calendario no banco de dados, use form.save() sem commit=False. 
            calendario = form.save(commit=False)  
            calendario.user = request.user # O campo 'user' é preenchido com o usuario logado.
            calendario.save() # O calendario é salvo no banco de dados.
            
            messages.success(request, 'Calendário cadastrado com sucesso!')
            return redirect('listar_calendarios')
        else:
            # Se o formulario não for valido, uma mensagem de erro é exibida.
            # O metodo render renderiza o template 'adicionar.html' e passa o contexto com o formulario.
            # no template, o formulario é acessado através da variável 'form'.
            messages.error(request, 'Erro ao cadastrar calendário.')
            return render(request, 'planner/calendario/adicionar.html', {
                'form': form
            })
    else:
        return redirect('adicionar_calendario')




# UC - Gerir calendário letivo
# Remove um calendario letivo que tenha um id especifico.
@login_required
@transaction.atomic
def remover_calendario(request, id):
    # O metodo get_object_or_404 busca o calendario com o id e do usuario logado.
    calendario = get_object_or_404(CalendarioLetivo, id=id, user=request.user)

    if request.method == 'POST':
        # O calendario é removido do banco de dados.
        calendario.delete()
        # Uma mensagem de sucesso é exibida.
        messages.success(request, 'Calendário removido com sucesso!')
        # redireciona para a lista de calendarios
        return redirect('listar_calendarios')


# UC - Gerir calendário letivo
# Exibe o formulário para editar um calendário letivo existente.
@login_required
def editar_calendario(request, id):
    # Busca o calendário com o id especificado e que pertence ao usuário logado
    calendario = get_object_or_404(CalendarioLetivo, id=id, user=request.user)
    
    # Cria um formulário preenchido com os dados do calendário existente
    form = CalendarioLetivoForm(instance=calendario)
    
    return render(request, 'planner/calendario/editar.html', {
        'form': form,
        'calendario': calendario
    })


# UC - Gerir planos de aula
# Exibe a lista de planos de aula de uma disciplina específica
@login_required
def listar_planos_aula(request, disciplina_id):
    # Busca a disciplina com o id especificado e que pertence ao usuário logado
    obj_disciplina = get_object_or_404(Disciplina, id=disciplina_id, user=request.user)

    # Busca todos os planos de aula da disciplina
    lista_planos = PlanoAula.objects.filter(disciplina=obj_disciplina)

    return render(request, 'planner/plano_aula/listar_planos_aula.html', {
        'disciplina': obj_disciplina,
        'planos': lista_planos
    })

# UC - Gerir planos de aula
# Processa o formulário de cadastro de um novo plano de aula
@login_required
@transaction.atomic
def cadastrar_plano_aula(request, disciplina_id):
    # Busca a disciplina com o id especificado e que pertence ao usuário logado
    obj_disciplina = get_object_or_404(Disciplina, id=disciplina_id, user=request.user)

    if request.method == 'POST':
        form = PlanoAulaForm(request.POST)

        if form.is_valid():
            plano = form.save(commit=False)
            plano.disciplina = obj_disciplina
            plano.save()
            messages.success(request, 'Plano de aula cadastrado com sucesso!')
            return redirect('listar_planos_aula', disciplina_id=disciplina_id)
        else:
            messages.error(request, 'Erro ao cadastrar plano de aula.')
            return render(request, 'planner/plano_aula/adicionar_plano_aula.html', {
                'form': form,
                'disciplina': obj_disciplina
            })
    else:
        return redirect('adicionar_plano_aula', disciplina_id=disciplina_id)

# UC - Gerir planos de aula
# Exibe o formulário para adicionar um novo plano de aula
@login_required
def adicionar_plano_aula(request, disciplina_id):
    # Busca a disciplina com o id especificado e que pertence ao usuário logado
    obj_disciplina = get_object_or_404(Disciplina, id=disciplina_id, user=request.user)

    if request.method == 'POST':
        # Cria um formulário com os dados do POST
        form = PlanoAulaForm(request.POST)

        if form.is_valid():
            # Associa o plano de aula à disciplina
            obj_plano = form.save(commit=False)
            obj_plano.disciplina = obj_disciplina
            obj_plano.save()
            messages.success(request, 'Plano de aula adicionado com sucesso!')
            return redirect('listar_planos_aula', disciplina_id=obj_disciplina.id)
    else:
        form = PlanoAulaForm()

    return render(request, 'planner/plano_aula/adicionar_plano_aula.html', {
        'form': form,
        'disciplina': obj_disciplina
    })

# UC - Gerir planos de aula
# Exibe o formulário para editar um plano de aula existente
@login_required
def editar_plano_aula(request, disciplina_id, plano_id):
    # Busca a disciplina e o plano de aula com os ids especificados
    obj_disciplina = get_object_or_404(Disciplina, id=disciplina_id, user=request.user)
    obj_plano = get_object_or_404(PlanoAula, id=plano_id)

    form = PlanoAulaForm(instance=obj_plano)

    return render(request, 'planner/plano_aula/editar_plano_aula.html', {
        'form': form,
        'disciplina': obj_disciplina,
        'plano': obj_plano
    })  


# UC - Gerir planos de aula
# Processa a atualização de um plano de aula existente
@login_required
@transaction.atomic
def atualizar_plano_aula(request, disciplina_id, plano_id):
    # Busca a disciplina e o plano de aula com os ids especificados
    obj_disciplina = get_object_or_404(Disciplina, id=disciplina_id, user=request.user)
    obj_plano = get_object_or_404(PlanoAula, id=plano_id)

    if request.method == 'POST':
        form = PlanoAulaForm(request.POST, instance=obj_plano)

        if form.is_valid():
            form.save()
            messages.success(request, 'Plano de aula atualizado com sucesso!')
            return redirect('listar_planos_aula', disciplina_id=obj_disciplina.id)
    else:
        form = PlanoAulaForm(instance=obj_plano)

    return render(request, 'planner/plano_aula/editar_plano_aula.html', {
        'form': form,
        'disciplina': obj_disciplina,
        'plano': obj_plano
    })

# UC - Gerir planos de aula
# Remove um plano de aula específico após confirmação
@login_required
@transaction.atomic
def remover_plano_aula(request, disciplina_id, plano_id):
    # Busca a disciplina e o plano de aula garantindo que pertencem ao usuário logado
    obj_disciplina = get_object_or_404(Disciplina, id=disciplina_id, user=request.user)
    obj_plano = get_object_or_404(PlanoAula, id=plano_id, disciplina=obj_disciplina)

    if request.method == 'POST':
        obj_plano.delete()
        messages.success(request, 'Plano de aula removido com sucesso!')
        return redirect('listar_planos_aula', disciplina_id=disciplina_id)

    return render(request, 'planner/plano_aula/remover_plano_aula.html', {
        'disciplina': obj_disciplina,
        'plano': obj_plano
    })


# UC - Gerir calendário letivo
# Atualiza um calendário letivo existente com os dados do formulário.
@login_required
@transaction.atomic
def atualizar_calendario(request, id):
    # Busca o calendário com o id especificado e que pertence ao usuário logado
    calendario = get_object_or_404(CalendarioLetivo, id=id, user=request.user)
    
    if request.method == 'POST':
        # Cria um formulário com os dados do POST e associa ao calendário existente
        form = CalendarioLetivoForm(request.POST, instance=calendario)
        
        if form.is_valid():
            # Salva as alterações no calendário
            form.save()
            messages.success(request, 'Calendário atualizado com sucesso!')
            return redirect('listar_calendarios')
        else:
            messages.error(request, 'Erro ao atualizar calendário.')
            return render(request, 'planner/calendario/editar.html', {
                'form': form,
                'calendario': calendario
            })
    else:
        return redirect('editar_calendario', id=id)
    

