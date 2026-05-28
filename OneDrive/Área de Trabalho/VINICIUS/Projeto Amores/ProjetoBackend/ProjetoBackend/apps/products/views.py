from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Count, F
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from core.utils import APIResponse, PaginationHelper
from .models import Product, Category
from .serializers import (
    ProductSerializer, ProductListSerializer, ProductCreateSerializer,
    ProductUpdateSerializer, CategorySerializer, StockUpdateSerializer
)


class ProductListCreateView(generics.ListCreateAPIView):
    """
    List and create products
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        return ProductListSerializer

    def get_queryset(self):
        queryset = Product.objects.select_related('category', 'created_by')

        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(sku__icontains=search) |
                Q(barcode__icontains=search)
            )

        # Category filter
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category_id=category)

        # Status filter
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)

        # Stock status filter
        stock_status = self.request.query_params.get('stock_status', None)
        if stock_status:
            if stock_status == 'out_of_stock':
                queryset = queryset.filter(stock_quantity=0)
            elif stock_status == 'low_stock':
                queryset = queryset.filter(
                    stock_quantity__gt=0,
                    stock_quantity__lte=models.F('min_stock_level')
                )
            elif stock_status == 'in_stock':
                queryset = queryset.filter(stock_quantity__gt=0)

        # Featured filter
        featured = self.request.query_params.get('featured', None)
        if featured is not None:
            queryset = queryset.filter(is_featured=featured.lower() == 'true')

        return queryset.order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return PaginationHelper.get_paginated_response(
            queryset, request, ProductListSerializer
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        response_serializer = ProductSerializer(product)
        return APIResponse.created(response_serializer.data)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update and delete product
    """
    queryset = Product.objects.select_related('category', 'created_by')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductUpdateSerializer
        return ProductSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        response_serializer = ProductSerializer(product)
        return APIResponse.success(response_serializer.data, _("Product updated successfully"))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return APIResponse.no_content(_("Product deleted successfully"))


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_stock_view(request, pk):
    """
    Update product stock
    """
    product = get_object_or_404(Product, pk=pk)
    serializer = StockUpdateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    quantity = serializer.validated_data['quantity']
    operation = serializer.validated_data['operation']

    if operation == 'set':
        product.stock_quantity = quantity
    elif operation == 'add':
        product.stock_quantity += quantity
    elif operation == 'subtract':
        product.stock_quantity = max(0, product.stock_quantity - quantity)

    product.save()

    response_serializer = ProductSerializer(product)
    return APIResponse.success(
        response_serializer.data,
        _("Stock updated successfully")
    )


class CategoryListCreateView(generics.ListCreateAPIView):
    """
    List and create categories
    """
    queryset = Category.objects.annotate(product_count=Count('products'))
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        return queryset.order_by('name')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        return APIResponse.created(serializer.data, _("Category created successfully"))


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update and delete category
    """
    queryset = Category.objects.annotate(product_count=Count('products'))
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        return APIResponse.success(serializer.data, _("Category updated successfully"))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if category has products
        if instance.products.exists():
            return APIResponse.error(
                _("Cannot delete category with existing products. Please reassign or delete products first."),
                status_code=status.HTTP_400_BAD_REQUEST
            )

        instance.delete()
        return APIResponse.no_content(_("Category deleted successfully"))


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def featured_products_view(request):
    """
    Get featured products (public endpoint)
    """
    products = Product.objects.filter(
        status='active',
        is_featured=True,
        stock_quantity__gt=0
    ).select_related('category')[:12]  # Limit to 12 featured products

    serializer = ProductListSerializer(products, many=True)
    return APIResponse.success(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def product_search_view(request):
    """
    Public product search
    """
    query = request.query_params.get('q', '')
    category = request.query_params.get('category', None)

    if not query and not category:
        return APIResponse.error(
            _("Search query or category is required"),
            status_code=status.HTTP_400_BAD_REQUEST
        )

    products = Product.objects.filter(status='active', stock_quantity__gt=0)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(sku__icontains=query)
        )

    if category:
        products = products.filter(category_id=category)

    products = products.select_related('category')[:50]  # Limit results
    serializer = ProductListSerializer(products, many=True)

    return APIResponse.success({
        'query': query,
        'results': serializer.data,
        'count': len(serializer.data)
    })