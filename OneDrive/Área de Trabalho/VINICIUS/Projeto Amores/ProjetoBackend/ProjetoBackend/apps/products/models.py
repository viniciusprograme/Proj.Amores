from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from decimal import Decimal


class Category(models.Model):
    """
    Product category model
    """
    name = models.CharField(
        _('name'),
        max_length=100,
        unique=True,
        help_text=_('Category name')
    )
    description = models.TextField(
        _('description'),
        blank=True,
        null=True,
        help_text=_('Category description')
    )
    slug = models.SlugField(
        _('slug'),
        unique=True,
        help_text=_('URL-friendly identifier')
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Whether this category is active')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Product model
    """
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('active', _('Active')),
        ('inactive', _('Inactive')),
        ('discontinued', _('Discontinued')),
    ]

    name = models.CharField(
        _('name'),
        max_length=200,
        help_text=_('Product name')
    )
    description = models.TextField(
        _('description'),
        blank=True,
        null=True,
        help_text=_('Product description')
    )
    sku = models.CharField(
        _('SKU'),
        max_length=50,
        unique=True,
        help_text=_('Stock Keeping Unit - unique product identifier')
    )
    barcode = models.CharField(
        _('barcode'),
        max_length=100,
        blank=True,
        null=True,
        help_text=_('Product barcode')
    )

    # Pricing
    price = models.DecimalField(
        _('price'),
        max_digits=10,
        decimal_places=2,
        help_text=_('Product price')
    )
    cost_price = models.DecimalField(
        _('cost price'),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('Product cost price')
    )
    discount_percentage = models.DecimalField(
        _('discount percentage'),
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text=_('Discount percentage (0-100)')
    )

    # Inventory
    stock_quantity = models.PositiveIntegerField(
        _('stock quantity'),
        default=0,
        help_text=_('Current stock quantity')
    )
    min_stock_level = models.PositiveIntegerField(
        _('minimum stock level'),
        default=0,
        help_text=_('Minimum stock level for reorder alerts')
    )
    max_stock_level = models.PositiveIntegerField(
        _('maximum stock level'),
        blank=True,
        null=True,
        help_text=_('Maximum stock level')
    )

    # Categories and relationships
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        help_text=_('Product category')
    )

    # Status and metadata
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        help_text=_('Product status')
    )
    is_featured = models.BooleanField(
        _('featured'),
        default=False,
        help_text=_('Whether this product is featured')
    )

    # Images
    image = models.ImageField(
        _('image'),
        upload_to='products/',
        blank=True,
        null=True,
        help_text=_('Product main image')
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Audit
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_products',
        help_text=_('User who created this product')
    )

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
            models.Index(fields=['is_featured']),
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def discounted_price(self):
        """Calculate discounted price"""
        if self.discount_percentage > 0:
            discount_amount = (self.price * self.discount_percentage) / 100
            return self.price - discount_amount
        return self.price

    @property
    def is_in_stock(self):
        """Check if product is in stock"""
        return self.stock_quantity > 0

    @property
    def stock_status(self):
        """Get stock status"""
        if self.stock_quantity <= 0:
            return 'out_of_stock'
        elif self.stock_quantity <= self.min_stock_level:
            return 'low_stock'
        else:
            return 'in_stock'

    @property
    def profit_margin(self):
        """Calculate profit margin percentage"""
        if self.cost_price and self.cost_price > 0:
            profit = self.price - self.cost_price
            return (profit / self.cost_price) * 100
        return None

    def save(self, *args, **kwargs):
        """Override save to handle SKU generation if not provided"""
        if not self.sku:
            # Generate SKU based on category and ID
            prefix = self.category.slug.upper()[:3] if self.category else 'PRD'
            # For new objects, we'll generate after save
            super().save(*args, **kwargs)
            if not self.sku:
                self.sku = f"{prefix}{self.id:06d}"
                # Call save again to update SKU
                super().save(update_fields=['sku'])
        else:
            super().save(*args, **kwargs)