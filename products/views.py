from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics
from .serializers import CategorySerializer, ProductSerializer, VariantSerializer
from .models import Category, Product, Variant
from .permissions import IsAdminOrShopkeeper
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

# ------- Categorias

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAdminOrShopkeeper()]
        return [AllowAny()]

# ------- Produtos

class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminOrShopkeeper()]
        return [AllowAny()]

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        return queryset

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method in ['PUT','PATCH','DELETE']:
            return [IsAdminOrShopkeeper()]
        return [AllowAny()]
    
    def patch(self, request, *args, **kwargs):
        product = self.get_object()
        data_updated = {'is_active': request.data.get('is_active', product.is_active)}
        serializer = self.get_serializer(product,data=data_updated,partial=True)
        serializer.is_valid()
        serializer.save()
        return Response({'id':product.id, 'is_active':product.is_active}, status=status.HTTP_200_OK)
        
# ------- Variações

class VariantListCreateView(generics.ListCreateAPIView):
    serializer_class = VariantSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminOrShopkeeper()]
        return [AllowAny()]
    
    def perform_create(self,serializer):
        product = get_object_or_404(Product, pk=self.kwargs['product_id'])
        serializer.save(product=product)

class VariantRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer
    permission_classes = [IsAdminOrShopkeeper,]
