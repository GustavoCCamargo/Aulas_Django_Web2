from django.db import models
from django.contrib.auth.models import User

class CalendarioLetivo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calendarios')
    nome = models.CharField(max_length=100)
    data_inicio = models.DateField()
    data_fim = models.DateField()

    def __str__(self):
        return self.nome

class DataImportante(models.Model):
    calendario = models.ForeignKey(CalendarioLetivo, on_delete=models.CASCADE, related_name='datas')
    data = models.DateField()
    detalhe = models.CharField(max_length=255)
    dia_letivo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.data} - {self.detalhe}"

class Disciplina(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='disciplinas')
    calendario = models.ForeignKey(CalendarioLetivo, on_delete=models.CASCADE, related_name='disciplinas')
    nome = models.CharField(max_length=100)
    objetivo = models.TextField(blank=True)
    ementa = models.TextField(blank=True)
    periodo = models.CharField(max_length=20)
    carga_horaria = models.PositiveIntegerField()

    def __str__(self):
        return self.nome

class PlanoAula(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='planos')
    data = models.DateField()
    titulo = models.CharField(max_length=100)
    objetivos = models.TextField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.titulo

class Tarefa(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='tarefas')
    plano_aula = models.ForeignKey(PlanoAula, on_delete=models.CASCADE, related_name='tarefas')
    descricao = models.TextField()
    prazo = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.descricao[:50]

class Avaliacao(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='avaliacoes')
    plano_aula = models.ForeignKey(PlanoAula, on_delete=models.CASCADE, related_name='avaliacoes')
    tipo = models.CharField(max_length=50)
    etapa = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    identificador = models.CharField(max_length=100)

    def __str__(self):
        return self.identificador
