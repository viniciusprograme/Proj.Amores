from django.contrib import admin
from .models import Agendamento


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'data_visita', 'horario_preferencial']
    list_filter = ['data_visita', 'horario_preferencial']
    search_fields = ['nome']
    date_hierarchy = 'data_visita'

# Para gerenciar os agendamentos pelo painel do admin
# Register your models here.
