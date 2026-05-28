from django.db import models
from django.conf import settings

class Agendamento(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agendamentos')
    data_visita = models.DateField(verbose_name="Data da Visita")
    horario_preferencial = models.TimeField(verbose_name="Horário da Visita")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['data_visita', 'horario_preferencial']

    def __str__(self):
        return f"Agendamento de {self.usuario.first_name or self.usuario.username} para {self.data_visita.strftime('%d/%m/%Y')} às {self.horario_preferencial.strftime('%H:%M')}"
