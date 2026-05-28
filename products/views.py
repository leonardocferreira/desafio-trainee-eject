from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CategorySerializer, ProductSerializer, VariantSerializer
from .models import Category, Product, Variant
from .permissions import IsAdminOrShopkeeper

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrShopkeeper,]

class VariantViewSet(viewsets.ModelViewSet):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer
    permission_classes = [IsAdminOrShopkeeper,]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrShopkeeper,]