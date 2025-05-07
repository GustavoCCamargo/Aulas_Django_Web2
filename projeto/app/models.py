from django.db import models

# Create your models here.
class Aluno(models.Model):
    nome = models.CharField()
    email = models.EmailField()
    idade = models.IntegerField()

class Professor(models.Model):
    nome = models.CharField(max_length= 100) 
        
class Disciplina(models.Model):
    nome = models.CharField(max_length= 100)
    professor = models.ForeignKey( Professor , on_delete = models . CASCADE ,related_name ='disciplinas')
    
class Tarefas(models.Model):
   disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
   titulo = models.CharField(max_length=100)     