from django.shortcuts import get_or_create
from rest_framework import generics
from .serializers import CartOwnerSerializer, CartItemSerializer
from .models import CartOwner, CartItem
from products.models import Variant
from .permissions import IsSelfOrAdmin

class CartOwnerRetrieveView(generics.RetrieveAPIView):
    serializer_class = CartOwnerSerializer

    def get_object(self):
        cart, _ = CartOwner.objects.get_or_create(user=self.request.user) # cria carrinho se não tiver
        return cart
    
class CartItemCreateView(generics.CreateAPIView):
    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        cart, _ = CartOwner.objects.get_or_create(user=self.request.user) # cria um carrinho se nao tiver
        product = Variant.objects.get(pk=serializer.validated_data['product_id'])
        quantity = serializer.validated_data['quantity']
        cart_item = CartItem.objects.filter(cart=cart, variant=product).first()
        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            CartItem.objects.create(cart=cart, variant=product, quantity=quantity)

class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsSelfOrAdmin,]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)
