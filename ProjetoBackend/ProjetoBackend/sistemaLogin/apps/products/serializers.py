from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer"""

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'description', 'slug', 'image',
            'is_active', 'order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    """Product serializer for management"""

    category_name = serializers.CharField(source='category.name', read_only=True)
    stock_status = serializers.CharField(read_only=True)
    discounted_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'short_description', 'price',
            'cost_price', 'discount_percentage', 'discounted_price',
            'stock_quantity', 'min_stock_level', 'sku', 'category',
            'category_name', 'status', 'is_featured', 'is_available',
            'main_image', 'slug', 'meta_title', 'meta_description',
            'stock_status', 'profit_margin', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'slug', 'sku', 'stock_status', 'discounted_price',
            'profit_margin', 'created_at', 'updated_at'
        ]


class ProductPublicSerializer(serializers.ModelSerializer):
    """Product serializer for public views (limited fields)"""

    category_name = serializers.CharField(source='category.name', read_only=True)
    discounted_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'short_description',
            'price', 'discounted_price', 'discount_percentage',
            'stock_quantity', 'category_name', 'is_featured',
            'main_image', 'slug'
        ]
        read_only_fields = fields