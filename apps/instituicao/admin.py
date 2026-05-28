from django.contrib import admin
from .models import Instituicao


@admin.register(Instituicao)
class InstituicaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'atualizado_em']
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao')
        }),
        ('Missão, Visão e Valores', {
            'fields': ('missao', 'visao', 'valores')
        }),
        ('Informações de Doação', {
            'fields': ('chave_pix', 'tipo_chave_pix')
        }),
        ('Contato', {
            'fields': ('telefone', 'email', 'endereco')
        }),
    )
