from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.name} - {self.created_at}'

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name = 'Products')
    name = models.CharField(max_length=255, verbose_name='Product Name')
    description = models.TextField(verbose_name='Product Description')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Product Price')
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['created_at', 'is_active']

    def __str__(self):
        return f'{self.name} - {self.created_at} - {self.is_active}'

class Variant(models.Model):
    class SizeChoices(models.TextChoices):
        SMALL = 'S', 'Small'
        MEDIUM = 'M', 'Medium'
        LARGE = 'L', 'Large'
        XLARGE = 'XL', 'X-Large'
    
    class ColorChoices(models.TextChoices):
        RED = 'RED', 'Red'
        BLUE = 'BLUE', 'Blue'
        GREEN = 'GREEN', 'Green'
        BLACK = 'BLACK', 'Black'
        WHITE = 'WHITE', 'White'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='Variants')
    size = models.CharField(max_length=10, choices=SizeChoices.choices, verbose_name='Variant Size')
    color = models.CharField(max_length=10, choices=ColorChoices.choices, verbose_name='Variant Color')
    stock = models.PositiveIntegerField(default=0, verbose_name='Stock Quantity')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Variant'
        verbose_name_plural = 'Variants'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.product.name} - {self.size} - {self.color} - {self.stock}'