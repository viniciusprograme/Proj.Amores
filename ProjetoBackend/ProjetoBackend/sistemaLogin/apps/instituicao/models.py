from django.db import models


class Instituicao(models.Model):
    """Modelo para armazenar informações da instituição Amores Instituto"""
    
    nome = models.CharField(max_length=255, default="Amores Instituto")
    descricao = models.TextField(
        default="O Instituto Amores é uma organização social sem fins lucrativos localizada no bairro Sapiranga, em Fortaleza–CE, dedicada à promoção de ações solidárias e ao fortalecimento da comunidade local."
    )
    missao = models.TextField(
        default="Promover o bem-estar social por meio de ações solidárias, contribuindo para a melhoria da qualidade de vida das pessoas e fortalecendo os laços comunitários."
    )
    visao = models.TextField(
        default="Ser referência em transformação social na comunidade, inspirando outras iniciativas e ampliando o alcance de nossas ações."
    )
    valores = models.TextField(
        default="Solidariedade, Empatia, Respeito, Compromisso social, Transparência"
    )
    
    # Informações de contato e doação
    chave_pix = models.CharField(max_length=255, default="00.000.000/0001-00")
    tipo_chave_pix = models.CharField(
        max_length=20, 
        default="CNPJ",
        choices=[
            ('CPF', 'CPF'),
            ('CNPJ', 'CNPJ'),
            ('EMAIL', 'Email'),
            ('TELEFONE', 'Telefone'),
            ('ALEATORIA', 'Aleatória'),
        ]
    )
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    endereco = models.CharField(max_length=255, default="Sapiranga, Fortaleza–CE")
    
    # Metadados
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Instituição"
        verbose_name_plural = "Instituições"
    
    def __str__(self):
        return self.nome
