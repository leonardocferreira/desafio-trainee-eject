from django.urls import path
from .views import CartOwnerRetrieveView, CartItemCreateView, CartItemDetailView

urlpatterns = [
    path('cart/', CartOwnerRetrieveView.as_view(), name='cart-owner'),
    path('cart/items/', CartItemCreateView.as_view(), name='cart-item-create'),
    path('cart/items/<int:pk>/', CartItemDetailView.as_view(), name='cart-item-detail'),
]



