from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Product CRUD
    path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/stock/', views.update_stock_view, name='product-stock-update'),

    # Category CRUD
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),

    # Public endpoints
    path('public/featured/', views.featured_products_view, name='featured-products'),
    path('public/search/', views.product_search_view, name='product-search'),
]