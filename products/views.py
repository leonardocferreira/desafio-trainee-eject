from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import CategorySerializer, ProductSerializer, VariantSerializer
from .models import Category, Product, Variant
from .permissions import IsAdminOrShopkeeper
from rest_framework.permissions import AllowAny

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.request.http in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAdminOrShopkeeper()]
        return [AllowAny()]

# class VariantViewSet(viewsets.ModelViewSet):
#     queryset = Variant.objects.all()
#     serializer_class = VariantSerializer
    
#     def get_permissions(self):
#         if self.request.http in ['POST', 'PUT', 'PATCH', 'DELETE']:
#             return [IsAdminOrShopkeeper()]
#         return [AllowAny()]

# # class ProductViewSet(viewsets.ModelViewSet):
# #     queryset = Product.objects.all()
# #     serializer_class = ProductSerializer
# #     permission_classes = [IsAdminOrShopkeeper,]

class VariantListCreateView(generics.ListCreateAPIView):
    pass

class VariantRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    pass

class ListCreateProductView(generics.ListCreateAPIView):
    pass

class RetrieveUpdateDestroyProductView(generics.RetrieveUpdateDestroyAPIView):
    pass