from django.db import models

# Create your models here.
class Aluno(models.Model):
    nome = models.CharField()
    email = models.EmailField()
    idade = models.IntegerField()