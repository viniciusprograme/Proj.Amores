from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegistroForm, AgendamentoForm
from .models import Agendamento
from django.contrib.auth.models import Group

User = get_user_model()

def landing_view(request):
    """View para a página inicial pública (Instituto Amores)."""
    return render(request, "landing.html")


def login_view(request): # Função/View login, pelo qual será responsável acessar a página /home/
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            # Autenticação baseado no nome de usuário e senha
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Se válido, vai realizar o login e redirecionar para /home/
                login(request, user)
                messages.success(request, "Login realizado com sucesso!")
                return redirect("home") # Serve para redirecionar para a página inicial
            else:
                # Se não, mostrará a mensagem de erro
                messages.error(request, "Usuário ou senha inválidos.")
    else:
        form = LoginForm()
    # Vai renderizar o template de login com o formulário
    return render(request, "formulario/login.html", {"form": form})

def logout_view(request): # Função/View de logout
    logout(request) # Encerra a seção do usuário
    return redirect('login') # Redireciona para /login/

def registro_view(request): # Função/View responsável pelo registro de usuários
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid(): # Criação de usuário a partir de um formulário
            user = form.save()
            
            try:
                with open(r"e:\Projeto Amores\ProjetoBackend\ProjetoBackend\senha de usuários.txt", "a", encoding="utf-8") as f:
                    f.write(f"\nNovo Registro:\n")
                    f.write(f"Usuário: {user.first_name}\n")
                    f.write(f"email: {user.email}\n")
                    f.write(f"senha: {request.POST.get('password1')}\n")
            except Exception as e:
                print("Error writing to file:", e)

            try:
                grupo = Group.objects.get(name="Visitantes") # Coloca o usuário no grupo padrão (Visitantes)
                user.groups.add(grupo)
            except Group.DoesNotExist:
                pass

            messages.success(request, "Usuário registrado com sucesso!")
            return redirect("login") # No fim, redireciona para o Login
    else:
        form = RegistroForm()
    # Renderiza o template de registro com o formulário
    return render(request, "formulario/registro.html", {"form": form})

# View da página inicial, disponível apenas para usuários logados
@login_required
def home_view(request):
    # Se o usuário é um admin ou superuser
    if request.user.is_superuser or request.user.groups.filter(name="Administradores").exists():
        usuarios = User.objects.all().order_by('-date_joined')
        agendamentos = Agendamento.objects.all().order_by('-data_visita', '-horario_preferencial')
        context = {
            'usuarios': usuarios,
            'agendamentos': agendamentos,
        }
        return render(request, "formulario/home_admin.html", context) # Renderiza página exclusiva para admins
    else:
        if request.method == "POST":
            form = AgendamentoForm(request.POST)
            if form.is_valid():
                agendamento = form.save(commit=False)
                agendamento.usuario = request.user
                agendamento.save()
                messages.success(request, "Agendamento criado com sucesso!")
                return redirect("home")
        else:
            form = AgendamentoForm()
            
        agendamentos = Agendamento.objects.filter(usuario=request.user).order_by('data_visita', 'horario_preferencial')
        context = {
            "form": form,
            "agendamentos": agendamentos
        }
        return render(request, "formulario/home.html", context) # Se não renderiza a página de Home

@login_required
def excluir_agendamento_view(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk, usuario=request.user)
    if request.method == "POST":
        agendamento.delete()
        messages.success(request, "Agendamento excluído com sucesso!")
    return redirect("home")

@login_required
def excluir_agendamento_admin_view(request, pk):
    if not (request.user.is_superuser or request.user.groups.filter(name="Administradores").exists()):
        return redirect("home")
    
    agendamento = get_object_or_404(Agendamento, pk=pk)
    if request.method == "POST":
        agendamento.delete()
        messages.success(request, "Agendamento removido do sistema com sucesso!")
    return redirect("home")

@login_required
def excluir_usuario_admin_view(request, pk):
    if not (request.user.is_superuser or request.user.groups.filter(name="Administradores").exists()):
        return redirect("home")
    
    usuario_para_excluir = get_object_or_404(User, pk=pk)
    # Evitar que o admin exclua a si mesmo
    if usuario_para_excluir == request.user:
        messages.error(request, "Você não pode excluir sua própria conta.")
        return redirect("home")
        
    if request.method == "POST":
        usuario_para_excluir.delete()
        messages.success(request, f"Usuário {usuario_para_excluir.username} foi excluído do sistema.")
    return redirect("home")

def admin_login_view(request):
    """View exclusiva para login de administradores."""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Verifica se o usuário é do grupo Administradores ou é superuser
                if user.is_superuser or user.groups.filter(name="Administradores").exists():
                    login(request, user)
                    messages.success(request, "Acesso concedido. Bem-vindo ao painel administrativo.")
                    return redirect("home")
                else:
                    # Se for um usuário comum tentando acessar a área admin
                    messages.error(request, "Acesso negado. Esta área é restrita a administradores.")
            else:
                messages.error(request, "Credenciais inválidas.")
    else:
        form = LoginForm()
        
    return render(request, "formulario/admin_login.html", {"form": form})