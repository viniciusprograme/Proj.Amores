#!/usr/bin/env python
"""
Script de setup automático para a integração Frontend-Backend
Execute com: python setup.py
"""

import os
import sys
import django
from pathlib import Path

# Adicionar o diretório do projeto ao path
project_dir = Path(__file__).parent / 'sistemaLogin'
sys.path.insert(0, str(project_dir))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistemaLogin.settings')
django.setup()

from django.core.management import call_command
from django.db import connection
from apps.instituicao.models import Instituicao

def run_migrations():
    """Executar migrações"""
    print("\n📋 Executando migrações...")
    try:
        call_command('makemigrations', 'instituicao')
        call_command('migrate')
        print("✅ Migrações executadas com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao executar migrações: {e}")
        return False

def create_default_instituicao():
    """Criar instituição padrão"""
    print("\n🏛️ Criando dados padrão da instituição...")
    try:
        instituicao, created = Instituicao.objects.get_or_create(
            nome="Amores Instituto"
        )
        
        if created:
            print("✅ Instituição criada com sucesso!")
            print(f"   - Nome: {instituicao.nome}")
            print(f"   - Chave PIX: {instituicao.chave_pix}")
            print(f"   - Endereço: {instituicao.endereco}")
        else:
            print("✅ Instituição já existe")
            
        return True
    except Exception as e:
        print(f"❌ Erro ao criar instituição: {e}")
        return False

def check_tables():
    """Verificar se as tabelas foram criadas"""
    print("\n📊 Verificando tabelas no banco de dados...")
    try:
        with connection.cursor() as cursor:
            # Listar todas as tabelas
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name LIKE '%instituicao%'
            """)
            instituicao_tables = cursor.fetchall()
            
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name LIKE '%agendamento%'
            """)
            agendamento_tables = cursor.fetchall()
            
        if instituicao_tables:
            print(f"✅ Tabelas de Instituição: {instituicao_tables}")
        if agendamento_tables:
            print(f"✅ Tabelas de Agendamento: {agendamento_tables}")
            
        return True
    except Exception as e:
        print(f"❌ Erro ao verificar tabelas: {e}")
        return False

def main():
    """Executar setup completo"""
    print("\n" + "="*60)
    print("🚀 SETUP DO BACKEND - AMORES INSTITUTO")
    print("="*60)
    
    steps = [
        ("Migrações", run_migrations),
        ("Dados Padrão", create_default_instituicao),
        ("Verificação", check_tables),
    ]
    
    results = []
    for step_name, step_func in steps:
        print(f"\n{'='*60}")
        print(f"Passo: {step_name}")
        print('='*60)
        results.append(step_func())
    
    print("\n" + "="*60)
    print("📊 RESUMO DO SETUP")
    print("="*60)
    
    if all(results):
        print("✅ Setup completado com sucesso!")
        print("\n🚀 Próximos passos:")
        print("   1. Inicie o servidor: python manage.py runserver")
        print("   2. Acesse o admin: http://localhost:8000/admin/")
        print("   3. Ou acesse a API: http://localhost:8000/api/v1/")
    else:
        print("❌ Setup incompleto. Verifique os erros acima.")
    
    print("="*60 + "\n")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        sys.exit(1)
