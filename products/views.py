from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics
from .serializers import CategorySerializer, ProductSerializer, VariantSerializer
from .models import Category, Product, Variant
from .permissions import IsAdminOrShopkeeper
from rest_framework.permissions import AllowAny

# ------- Categorias

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.request.http in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAdminOrShopkeeper()]
        return [AllowAny()]

# ------- Variações

class VariantListCreateView(generics.ListCreateAPIView):
    serializer_class = VariantSerializer

    def get_permissions(self):
        if self.request.http == 'POST':
            return [IsAdminOrShopkeeper()]
        return [AllowAny()]
    
    def perform_create(self,serializer):
        product = get_object_or_404(Product, pk=self.kwargs['product_id'])
        serializer.save(product=product)

class VariantRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer

# ------- Produtos

class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.http == 'POST':
            return [IsAdminOrShopkeeper()]
        return [AllowAny()]

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        return queryset

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.http in ['PUT','DELETE']:
            return [IsAdminOrShopkeeper()]
        return [AllowAny()]