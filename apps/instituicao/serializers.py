from rest_framework import serializers
from .models import Instituicao


class InstituicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instituicao
        fields = [
            'id',
            'nome',
            'descricao',
            'missao',
            'visao',
            'valores',
            'chave_pix',
            'tipo_chave_pix',
            'telefone',
            'email',
            'endereco',
        ]
