from django.urls import path, include
from .views import CategoryViewSet, VariantListCreateView, VariantRetrieveUpdateDeleteView, ProductListCreateView, ProductRetrieveUpdateDestroyView
from rest_framework.routers import DefaultRouter

productRouter = DefaultRouter()
productRouter.register('categories', CategoryViewSet, basename='categories')


urlpatterns = [
    path('', include(productRouter.urls)),

    path('products/', ProductListCreateView.as_view(), name='list_create_products'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='detail_produtcs'),

    path('products/<int:product_id>/variations/', VariantListCreateView.as_view(),name='list_create_variant'),
    path('variations/<int:pk>/', VariantRetrieveUpdateDeleteView.as_view(), name='detail_variant')
    ]
