from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""

    product_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'description', 'slug', 'is_active',
            'created_at', 'updated_at', 'product_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_product_count(self, obj):
        return obj.products.filter(status='active').count()


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model"""

    category_name = serializers.CharField(source='category.name', read_only=True)
    discounted_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    stock_status = serializers.CharField(read_only=True)
    profit_margin = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    created_by_name = serializers.CharField(
        source='created_by.get_full_name', read_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'sku', 'barcode',
            'price', 'cost_price', 'discount_percentage', 'discounted_price',
            'stock_quantity', 'min_stock_level', 'max_stock_level',
            'category', 'category_name', 'status', 'is_featured',
            'image', 'stock_status', 'profit_margin',
            'created_at', 'updated_at', 'created_by', 'created_by_name'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'discounted_price',
            'stock_status', 'profit_margin', 'created_by_name'
        ]

    def validate_price(self, value):
        """Validate price is positive"""
        if value <= 0:
            raise serializers.ValidationError(_("Price must be greater than zero."))
        return value

    def validate_discount_percentage(self, value):
        """Validate discount percentage is between 0 and 100"""
        if not (0 <= value <= 100):
            raise serializers.ValidationError(_("Discount percentage must be between 0 and 100."))
        return value

    def validate_sku(self, value):
        """Validate SKU uniqueness"""
        queryset = Product.objects.filter(sku=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError(_("SKU must be unique."))
        return value


class ProductCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating products"""

    class Meta:
        model = Product
        fields = [
            'name', 'description', 'sku', 'barcode',
            'price', 'cost_price', 'discount_percentage',
            'stock_quantity', 'min_stock_level', 'max_stock_level',
            'category', 'status', 'is_featured', 'image'
        ]

    def create(self, validated_data):
        """Create product with created_by field"""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer for product listing (lighter version)"""

    category_name = serializers.CharField(source='category.name', read_only=True)
    discounted_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    stock_status = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'price', 'discounted_price',
            'stock_quantity', 'category_name', 'status',
            'is_featured', 'image', 'stock_status', 'updated_at'
        ]


class ProductUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating products"""

    class Meta:
        model = Product
        fields = [
            'name', 'description', 'sku', 'barcode',
            'price', 'cost_price', 'discount_percentage',
            'stock_quantity', 'min_stock_level', 'max_stock_level',
            'category', 'status', 'is_featured', 'image'
        ]


class StockUpdateSerializer(serializers.Serializer):
    """Serializer for stock updates"""

    quantity = serializers.IntegerField(min_value=0)
    operation = serializers.ChoiceField(
        choices=['set', 'add', 'subtract'],
        default='set'
    )

    def validate_quantity(self, value):
        """Validate quantity"""
        if value < 0:
            raise serializers.ValidationError(_("Quantity cannot be negative."))
        return value