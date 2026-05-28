from django.urls import path, include
from .views import CategoryViewSet, ProductViewSet, VariantViewSet
from rest_framework.routers import DefaultRouter

productRouter = DefaultRouter
productRouter.register(r'categories', CategoryViewSet, basename='category')
productRouter.register(r'products', ProductViewSet, basename='product')
productRouter.register(r'variants', VariantViewSet, basename='variant')

urlpatterns = [
    path('', include(productRouter.urls)),
    ]
