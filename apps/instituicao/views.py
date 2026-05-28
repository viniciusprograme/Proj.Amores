from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Instituicao
from .serializers import InstituicaoSerializer


class InstituicaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para informações da Instituição Amores
    """
    queryset = Instituicao.objects.all()
    serializer_class = InstituicaoSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def principal(self, request):
        """Retorna os dados principais da instituição"""
        try:
            instituicao = Instituicao.objects.first()
            if not instituicao:
                # Criar instituição padrão se não existir
                instituicao = Instituicao.objects.create()
            
            serializer = self.get_serializer(instituicao)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
