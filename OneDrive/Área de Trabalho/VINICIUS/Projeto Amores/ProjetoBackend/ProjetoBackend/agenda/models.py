from django.db import models

class Agendamento(models.Model): 
    nome = models.CharField(max_length=200) # Nome da pessoa que vai visitar
    data_visita = models.DateField() # Data da visita
    horario_preferencial = models.TimeField() # Horário de preferência

    def __str__(self):
        return f"{self.nome} - {self.data_visita} às {self.horario_preferencial}" # Retorna mensagem dizendo o nome, data e horário do agendamento
# Create your models here.
