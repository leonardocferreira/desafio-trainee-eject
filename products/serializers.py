from rest_framework import serializers
from .models import Category, Product, Variant

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'created_at',
            'updated_at',
        ]

    def validate_name(self, value):
        if Category.objects.filter(name=value.lower()).exists():
            raise serializers.ValidationError("A category with this name already exists.")
        return value

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        extra_kwargs = {
        'size': {'required': True},
        'color': {'required': True},
        'stock': {'required': True},
        }
        read_only_fields = ['product','created_at', 'updated_at']
        fields = [
            'id',
            'product',
            'size',
            'color',
            'stock',
            'created_at',
            'updated_at',
        ]

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value

class ProductSerializer(serializers.ModelSerializer):
    variations = VariantSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    extra_kwargs = {
        'name': {'required': True},
        'description': {'required': True},
        'price': {'required': True},
        'is_active': {'required': True},
    }
    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'category_id',
            'name',
            'description',
            'price',
            'variations',
            'is_active',
            'created_at',
            'updated_at',
        ]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive number.")
        return value