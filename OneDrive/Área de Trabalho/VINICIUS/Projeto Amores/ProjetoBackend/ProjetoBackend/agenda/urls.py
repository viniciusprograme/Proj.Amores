from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router para API REST
router = DefaultRouter()
router.register(r'api', views.AgendamentoViewSet, basename='agendamento-api')

urlpatterns = [ 
    path("agendamentos/", views.listar_agendamentos, name="listar_agendamentos"),
    path("agendamentos/novo/", views.criar_agendamento, name="criar_agendamento"),
    path("", include(router.urls)),
]
# Rotas das páginas para o projeto principal