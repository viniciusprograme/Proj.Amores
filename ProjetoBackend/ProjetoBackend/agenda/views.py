from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .forms import AgendamentoForm
from .models import Agendamento
from .serializers import AgendamentoSerializer

@login_required
def criar_agendamento(request): # View para criação de agendamento
    if request.method == "POST":
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            form.save() # Salva no banco usando o Model
            return redirect("listar_agendamentos") # Redireciona para a página listar_agendamentos
    else:
        form = AgendamentoForm()
    return render(request, "agenda/criar_agendamento.html", {"form": form}) # Renderiza a página de criação de agendamentos

@login_required
def listar_agendamentos(request):
    agendamentos = Agendamento.objects.all()
    return render(request, "agenda/listar_agendamentos.html", {"agendamentos": agendamentos}) # Renderiza a página que lista os agendamentos


# API ViewSet para agendamentos
class AgendamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar agendamentos de visitas
    """
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        """Criar novo agendamento"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(
                {
                    'message': 'Agendamento realizado com sucesso!',
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def listar(self, request):
        """Listar todos os agendamentos"""
        agendamentos = self.get_queryset()
        serializer = self.get_serializer(agendamentos, many=True)
        return Response(serializer.data)
