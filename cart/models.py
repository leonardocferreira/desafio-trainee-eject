from django.db import models
from user.models import UserModel
from products.models import Variant

class CartOwner(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='cart_owner')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cart Owner'
        verbose_name_plural = 'Cart Owners'

    def __str__(self):
        return f'CartOwner: {self.user.email}'
    
class CartItem(models.Model):
    cart = models.ForeignKey(CartOwner, on_delete=models.CASCADE, related_name='cart_items')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name='Quantity')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        unique_together = ('cart', 'variant'),

    def __str__(self):
        return f''