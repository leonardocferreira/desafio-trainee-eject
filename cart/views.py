from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .serializers import CartOwnerSerializer, CartItemSerializer
from .models import CartOwner, CartItem
from .permissions import IsSelfOrAdmin
from products.models import Variant

class CartOwnerRetrieveView(generics.RetrieveAPIView):
    serializer_class = CartOwnerSerializer

    def get_object(self):
        cart, _ = CartOwner.objects.get_or_create(user=self.request.user) # cria um carrinho se não tiver
        return cart
    
class CartItemCreateView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsSelfOrAdmin,]

    def perform_create(self, serializer):
        cart, _ = CartOwner.objects.get_or_create(user=self.request.user) # cria um carrinho se não tiver
        variant = get_object_or_404(Variant, pk=serializer.validated_data['variant_id'])
        quantity = serializer.validated_data['quantity']
        existing_item = CartItem.objects.filter(cart=cart, variant=variant).first()
        if existing_item:
            total_quantity = quantity + existing_item.quantity
            if total_quantity > variant.stock:
                raise ValidationError(f'Invalid quantity. We only have {variant.stock} in stock.')
            existing_item.quantity = total_quantity
            existing_item.save()
            serializer.instance = existing_item
        else:
            serializer.save(cart=cart, variant=variant, quantity=quantity)

class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsSelfOrAdmin,]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_update(self, serializer):
        pass
