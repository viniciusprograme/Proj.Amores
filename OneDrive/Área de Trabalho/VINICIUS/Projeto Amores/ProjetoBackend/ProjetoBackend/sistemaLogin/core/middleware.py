from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth.models import AnonymousUser
from django.conf import settings


class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware that adds JWT authentication to requests.
    This is optional authentication - if token is invalid or missing,
    request.user remains AnonymousUser.
    """

    def process_request(self, request):
        """
        Process the request to authenticate user if JWT token is present.
        """
        # Skip authentication for certain paths
        exempt_paths = getattr(settings, 'JWT_AUTH_EXEMPT_PATHS', [
            '/admin/',
            '/api/schema/',
            '/api/docs/',
            '/api/redoc/',
        ])

        if any(request.path.startswith(path) for path in exempt_paths):
            return

        # Try to get token from Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return

        token_string = auth_header.split(' ')[1]

        try:
            # Validate token
            token = AccessToken(token_string)

            # Get user from token
            user_id = token.payload.get('user_id')
            if user_id:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                try:
                    user = User.objects.get(id=user_id)
                    request.user = user
                except User.DoesNotExist:
                    pass

        except (InvalidToken, TokenError, KeyError):
            # Token is invalid, but we don't raise an error
            # Just leave request.user as AnonymousUser
            pass