from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from . import serializers

User = get_user_model()


class AuthViewSet(viewsets.ViewSet):
    """
    Authentication endpoints
    """

    @action(detail=False, methods=['post'], permission_classes=[])
    def register(self, request):
        """Register a new user"""
        serializer = serializers.UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': serializers.UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[])
    def login(self, request):
        """Login user"""
        serializer = serializers.UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'user': serializers.UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                })
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def token_refresh(self, request):
        """Refresh access token"""
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'error': 'Refresh token required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken(refresh_token)
            return Response({
                'access': str(refresh.access_token)
            })
        except Exception:
            return Response(
                {'error': 'Invalid refresh token'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class UserViewSet(viewsets.ModelViewSet):
    """
    User management endpoints
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset based on user permissions"""
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """Update current user profile"""
        serializer = serializers.UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminUserListView(generics.ListAPIView):
    """
    Admin view for listing all users
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = User.objects.all()
        # Add filtering options
        email = self.request.query_params.get('email', None)
        is_active = self.request.query_params.get('is_active', None)

        if email:
            queryset = queryset.filter(email__icontains=email)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        return queryset