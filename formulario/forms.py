from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Agendamento
User = get_user_model()

class LoginForm(forms.Form): # Classe dedicada a Login (Usuário e senha)
    username = forms.CharField(label = "E-mail")
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")

class RegistroForm(UserCreationForm): # Classe para cadastro de usuários no sistema
    class Meta:
        model = User
        fields = ["first_name", "email"]

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['data_visita', 'horario_preferencial']
        widgets = {
            'data_visita': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',
                'required': 'required'
            }),
            'horario_preferencial': forms.TimeInput(attrs={
                'type': 'time', 
                'class': 'form-control', 
                'min': '08:00', 
                'max': '18:00',
                'required': 'required',
                'title': 'Selecione um horário comercial (08:00 às 18:00)'
            }),
        }
