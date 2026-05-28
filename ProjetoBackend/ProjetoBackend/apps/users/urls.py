from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from . import views

app_name = 'users'

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.UserRegistrationView.as_view(), name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/change-password/', views.change_password_view, name='change-password'),

    # JWT token management
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token-verify'),

    # User profile endpoints
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('me/', views.current_user_view, name='current-user'),

    # Admin endpoints
    path('admin/users/', views.UserListView.as_view(), name='user-list'),
]