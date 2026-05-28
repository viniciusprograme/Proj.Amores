from django.urls import path
from .views import login_view, logout_view, home_view, registro_view, landing_view, excluir_agendamento_view, excluir_agendamento_admin_view, excluir_usuario_admin_view, admin_login_view

urlpatterns = [
    path('', landing_view, name='landing'), # Rota inicial pública (Instituto Amores)
    path('login/', login_view, name='login'), # Rota para Login
    path('logout/', logout_view, name='logout'), # Rota para Logout
    path('home/', home_view, name='home'), # Rota para Home
    path('registro/', registro_view, name='registro'), # Rota para Registro
    path('excluir-agendamento/<int:pk>/', excluir_agendamento_view, name='excluir_agendamento'),
    path('admin/excluir-agendamento/<int:pk>/', excluir_agendamento_admin_view, name='excluir_agendamento_admin'),
    path('admin/excluir-usuario/<int:pk>/', excluir_usuario_admin_view, name='excluir_usuario_admin'),
    path('admin-login/', admin_login_view, name='admin_login'),
]

# Rotas de URLs da aplicação formulario para o projeto sistemaLogin