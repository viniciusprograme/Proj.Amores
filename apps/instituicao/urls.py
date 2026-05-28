from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InstituicaoViewSet

router = DefaultRouter()
router.register(r'', InstituicaoViewSet, basename='instituicao')

urlpatterns = [
    path('', include(router.urls)),
]
