from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for ViewSets
# router = DefaultRouter()
# router.register(r'categories', views.CategoryViewSet, basename='categories')
# router.register(r'products', views.ProductViewSet, basename='products')

# Public URLs (no authentication required)
public_patterns = [
    path('featured/', views.FeaturedProductsView.as_view(), name='featured-products'),
    path('search/', views.ProductSearchView.as_view(), name='product-search'),
]

urlpatterns = [
    # path('', include(router.urls)),
    path('public/', include(public_patterns)),
]