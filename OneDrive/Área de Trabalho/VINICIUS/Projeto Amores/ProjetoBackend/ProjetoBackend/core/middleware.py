from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
import logging

logger = logging.getLogger(__name__)


class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware para autenticação JWT opcional.
    Permite acesso público a rotas não protegidas e autenticação JWT para rotas protegidas.
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Processa a autenticação JWT se o token estiver presente no header Authorization.
        """
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

            try:
                # Valida o token JWT
                access_token = AccessToken(token)
                request.user_id = access_token['user_id']
                request.token_payload = access_token.payload
                logger.info(f"Token válido para usuário {request.user_id}")

            except (InvalidToken, TokenError) as e:
                logger.warning(f"Token inválido: {str(e)}")
                return JsonResponse({
                    'error': 'Token inválido ou expirado',
                    'code': 'INVALID_TOKEN'
                }, status=401)

            except Exception as e:
                logger.error(f"Erro na autenticação JWT: {str(e)}")
                return JsonResponse({
                    'error': 'Erro interno na autenticação',
                    'code': 'AUTH_ERROR'
                }, status=500)

        return None