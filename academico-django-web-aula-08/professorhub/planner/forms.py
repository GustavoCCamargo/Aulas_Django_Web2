from django import forms


"""
CalendarioLetivoForm é um ModelForm do Django que facilita a criação e edição de instâncias do modelo CalendarioLetivo através de formulários HTML.

No Django, um ModelForm é uma classe que cria automaticamente campos de formulário baseados nos campos de um modelo especificado. 
Isso reduz a necessidade de criar manualmente cada campo do formulário.

Neste caso, o CalendarioLetivoForm:
- Está vinculado ao modelo CalendarioLetivo.
- Inclui os campos 'nome', 'data_inicio' e 'data_fim' no formulário.
- Utiliza widgets personalizados para os campos de data, exibindo-os como campos do tipo 'date' no HTML, o que permite ao usuário selecionar datas usando um seletor de datas do navegador.

# Comentário para o código:
# Este ModelForm gera automaticamente um formulário HTML baseado no modelo CalendarioLetivo,
# facilitando a validação e o salvamento dos dados no banco de dados.
"""
from .models import CalendarioLetivo, Disciplina, PlanoAula

# 
class CalendarioLetivoForm(forms.ModelForm):
    class Meta:
        model = CalendarioLetivo
        fields = ['nome', 'data_inicio', 'data_fim']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }


"""
O método __init__ abaixo é um construtor que personaliza a inicialização do DisciplinaForm.
Ele executa as seguintes tarefas:

1. Aceita argumentos padrão do formulário (*args, **kwargs) e um parâmetro adicional 'user'
2. Extrai o usuário de kwargs para evitar passá-lo para a classe pai
3. Chama o construtor da classe pai com os argumentos restantes
4. Se um usuário for fornecido, filtra o queryset do campo 'calendario' para mostrar apenas
   os calendários pertencentes ao usuário logado

Esta personalização garante que os usuários só possam selecionar calendários que possuem ao
criar ou editar uma Disciplina, implementando uma forma básica de controle de acesso.
"""
class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome', 'calendario', 'objetivo', 'ementa', 'periodo', 'carga_horaria']
        widgets = {
            'objetivo': forms.Textarea(attrs={'rows': 3}),
            'ementa': forms.Textarea(attrs={'rows': 3}),
        }
    

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(DisciplinaForm, self).__init__(*args, **kwargs)
        if user:
            # Filtra os calendários para mostrar apenas os do usuário logado
            self.fields['calendario'].queryset = CalendarioLetivo.objects.filter(user=user)


"""
PlanoAulaForm é um ModelForm para o modelo PlanoAula.
Este formulário permite a criação e edição de planos de aula para uma disciplina específica.
Inclui campos para data, título, objetivos e status do plano de aula.
"""
class PlanoAulaForm(forms.ModelForm):
    class Meta:
        model = PlanoAula
        fields = ['data', 'titulo', 'objetivos', 'status']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'objetivos': forms.Textarea(attrs={'rows': 3}),
        }
    

