from django import forms
from .models import Agendamento

class AgendamentoForm(forms.ModelForm): # Gera um formulário com os campos modelo Agendamento
    class Meta:
        model = Agendamento
        fields = ["nome", "data_visita", "horario_preferencial"]