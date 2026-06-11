from rest_framework import serializers
from .models import CartOwner, CartItem
from products.models import Variant

class CartItemSerializer(serializers.ModelSerializer):
    variant = serializers.StringRelatedField(source='variant')
    variant_name = serializers.PrimaryKeyRelatedField(queryset=Variant.objects.all())

    class Meta:
        model = CartItem
        fields = [
            'id',
            'variant',
            'variant_name',
            'quantity',
        ]

    def validate(self, attrs):
        quantity = attrs['quantity']
        variant = attrs['variant']
        if quantity > variant.stock: 
            raise serializers.ValidationError(f'Invalid quantity. We only have {variant.stock} in stock.')
        return attrs

class CartOwnerSerializer(serializers.ModelSerializer):
    itens = CartItemSerializer(source='cart_items', many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.id')
    user_name = serializers.ReadOnlyField(source='user.name') 

    class Meta:
        model = CartOwner
        fields = [
            'id',
            'user',
            'user_name',
            'itens',
        ]
