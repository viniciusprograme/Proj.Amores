from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


class APIResponse:
    """Classe utilitária para padronizar respostas da API"""

    @staticmethod
    def success(data=None, message="Operação realizada com sucesso", status_code=status.HTTP_200_OK):
        """Retorna resposta de sucesso padronizada"""
        response_data = {
            'success': True,
            'message': message,
        }
        if data is not None:
            response_data['data'] = data

        logger.info(f"API Success: {message}")
        return Response(response_data, status=status_code)

    @staticmethod
    def error(message="Erro interno do servidor", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        """Retorna resposta de erro padronizada"""
        response_data = {
            'success': False,
            'message': message,
        }
        if errors:
            response_data['errors'] = errors

        logger.error(f"API Error: {message}")
        return Response(response_data, status=status_code)

    @staticmethod
    def created(data=None, message="Recurso criado com sucesso"):
        """Retorna resposta de criação padronizada"""
        return APIResponse.success(data, message, status.HTTP_201_CREATED)

    @staticmethod
    def no_content(message="Recurso removido com sucesso"):
        """Retorna resposta de remoção padronizada"""
        return APIResponse.success(message=message, status_code=status.HTTP_204_NO_CONTENT)


class PaginationHelper:
    """Helper para paginação padronizada"""

    @staticmethod
    def get_paginated_response(queryset, request, serializer_class):
        """Retorna resposta paginada padronizada"""
        from rest_framework.pagination import PageNumberPagination

        paginator = PageNumberPagination()
        paginator.page_size = 20
        paginator.page_size_query_param = 'page_size'
        paginator.max_page_size = 100

        page = paginator.paginate_queryset(queryset, request)
        serializer = serializer_class(page, many=True)

        return paginator.get_paginated_response(serializer.data)