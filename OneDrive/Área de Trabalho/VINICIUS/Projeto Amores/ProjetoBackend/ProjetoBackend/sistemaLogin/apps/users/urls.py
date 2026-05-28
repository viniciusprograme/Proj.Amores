from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for ViewSets
# router = DefaultRouter()
# router.register(r'auth', views.AuthViewSet, basename='auth')
# router.register(r'', views.UserViewSet, basename='users')

# Admin URLs
admin_patterns = [
    path('users/', views.AdminUserListView.as_view(), name='admin-users'),
]

urlpatterns = [
    # path('', include(router.urls)),
    path('admin/', include(admin_patterns)),
]