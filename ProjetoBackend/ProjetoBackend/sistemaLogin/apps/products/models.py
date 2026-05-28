from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from apps.users.models import User


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
        help_text=_('Category description')
    )

    slug = models.SlugField(
        _('slug'),
        max_length=120,
        unique=True,
        blank=True,
        help_text=_('URL-friendly version of the name')
    )

    image = models.ImageField(
        _('image'),
        upload_to='categories/',
        blank=True,
        null=True,
        help_text=_('Category image')
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Whether this category is active')
    )

    # Ordering
    order = models.PositiveIntegerField(
        _('order'),
        default=0,
        help_text=_('Display order')
    )

    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    # Metadata
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_categories',
        help_text=_('User who created this category')
    )

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


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

    # Basic information
    name = models.CharField(
        _('name'),
        max_length=200,
        help_text=_('Product name')
    )

    description = models.TextField(
        _('description'),
        blank=True,
        help_text=_('Product description')
    )

    short_description = models.CharField(
        _('short description'),
        max_length=300,
        blank=True,
        help_text=_('Brief product description for listings')
    )

    # Pricing
    price = models.DecimalField(
        _('price'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text=_('Product price')
    )

    cost_price = models.DecimalField(
        _('cost price'),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text=_('Product cost price (for profit calculations)')
    )

    discount_percentage = models.DecimalField(
        _('discount percentage'),
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
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
        help_text=_('Minimum stock level before reorder')
    )

    sku = models.CharField(
        _('SKU'),
        max_length=100,
        unique=True,
        blank=True,
        help_text=_('Stock Keeping Unit')
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

    # Status and visibility
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

    is_available = models.BooleanField(
        _('available'),
        default=True,
        help_text=_('Whether this product is available for purchase')
    )

    # Images
    main_image = models.ImageField(
        _('main image'),
        upload_to='products/',
        blank=True,
        null=True,
        help_text=_('Main product image')
    )

    # SEO and metadata
    slug = models.SlugField(
        _('slug'),
        max_length=220,
        unique=True,
        blank=True,
        help_text=_('URL-friendly version of the name')
    )

    meta_title = models.CharField(
        _('meta title'),
        max_length=60,
        blank=True,
        help_text=_('SEO meta title')
    )

    meta_description = models.CharField(
        _('meta description'),
        max_length=160,
        blank=True,
        help_text=_('SEO meta description')
    )

    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    # Metadata
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_products',
        help_text=_('User who created this product')
    )

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'is_featured']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['price']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.sku:
            # Generate SKU if not provided
            import uuid
            self.sku = f"PRD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    @property
    def discounted_price(self):
        """
        Calculate discounted price
        """
        if self.discount_percentage > 0:
            discount_amount = (self.price * self.discount_percentage) / 100
            return self.price - discount_amount
        return self.price

    @property
    def stock_status(self):
        """
        Get stock status
        """
        if self.stock_quantity <= 0:
            return 'out_of_stock'
        elif self.stock_quantity <= self.min_stock_level:
            return 'low_stock'
        else:
            return 'in_stock'

    @property
    def profit_margin(self):
        """
        Calculate profit margin if cost_price is available
        """
        if self.cost_price and self.cost_price > 0:
            return ((self.price - self.cost_price) / self.price) * 100
        return None

    def is_in_stock(self):
        """
        Check if product is in stock
        """
        return self.stock_quantity > 0 and self.is_available

    def can_be_ordered(self, quantity=1):
        """
        Check if product can be ordered with given quantity
        """
        return self.is_in_stock() and self.stock_quantity >= quantity