from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from . import serializers
from .models import Category, Product


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Category management endpoints
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'order', 'created_at']
    ordering = ['order', 'name']


class ProductViewSet(viewsets.ModelViewSet):
    """
    Product management endpoints
    """
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'category', 'is_featured', 'created_by']
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['name', 'price', 'created_at', 'stock_quantity']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter queryset based on user permissions"""
        queryset = Product.objects.all()

        # If not admin, only show active products or user's own products
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                Q(status='active') | Q(created_by=self.request.user)
            )

        return queryset

    def perform_create(self, serializer):
        """Set created_by when creating product"""
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_stock(self, request, pk=None):
        """Update product stock"""
        product = self.get_object()
        stock_quantity = request.data.get('stock_quantity')

        if stock_quantity is not None:
            product.stock_quantity = stock_quantity
            product.save()
            serializer = self.get_serializer(product)
            return Response(serializer.data)
        return Response(
            {'error': 'stock_quantity is required'},
            status=400
        )


class FeaturedProductsView(generics.ListAPIView):
    """
    Public view for featured products
    """
    serializer_class = serializers.ProductPublicSerializer
    permission_classes = [AllowAny]
    queryset = Product.objects.filter(
        status='active',
        is_featured=True,
        is_available=True
    ).select_related('category').order_by('-created_at')


class ProductSearchView(generics.ListAPIView):
    """
    Public search view for products
    """
    serializer_class = serializers.ProductPublicSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['name', 'price']
    ordering = ['name']

    def get_queryset(self):
        queryset = Product.objects.filter(
            status='active',
            is_available=True
        ).select_related('category')

        query = self.request.query_params.get('q', '')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(sku__icontains=query)
            )

        return queryset