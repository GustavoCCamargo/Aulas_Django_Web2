from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.

def submit_login(request):
    if request.method == 'POST':
        email = request.POST.get('loginEmail')
        senha = request.POST.get('loginPassword')

        if email and senha:
            user = authenticate(username=email, password=senha)
            if user is not None:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Credenciais inválidas. Verifique e tente novamente.")
        else:
            messages.error(request, "Preencha todos os campos.")
        return redirect('index')  # redireciona de volta para a tela de login
    else:
        messages.error(request, "Erro ao processar requisição.")
        return redirect('index')



def submit_register(request):
    if request.method == 'POST':
        nome = request.POST.get('registerName')
        pwd = request.POST.get('registerPassword')
        correio_eletronico = request.POST.get('registerEmail')

        if nome and pwd and correio_eletronico:
            # Verifica se já existe um usuário com o mesmo e-mail
            if User.objects.filter(username=correio_eletronico).exists():
                messages.error(request, "Email já cadastrado. Escolha outro ou tente fazer o login.")
                return redirect('index')
            try:
                # Cria o novo usuário
                novo_usuario = User.objects.create_user(
                    username=correio_eletronico,
                    email=correio_eletronico,
                    password=pwd,
                    first_name=nome
                )

                # Autentica e faz login
                user = authenticate(username=correio_eletronico, password=pwd)
                if user is not None:
                    login(request, user)
                    return redirect('admin_dashboard')

                else:
                    messages.error(request, "Usuário criado, mas falha ao autenticar.")
                    return redirect('index')
            except Exception as e:
                messages.error(request, f"Erro ao criar usuário: {e}")
                return redirect('index')
                
        else:
            messages.error(request, "Algum campo está vazio.")
            return redirect('index')
            
    else:
        
        messages.error(request, "Erro ao processar.")
        return redirect('index')


def logout_view(request):
    logout(request)
    messages.success(request, "Você saiu da sua conta com sucesso.")
    return redirect('index') 