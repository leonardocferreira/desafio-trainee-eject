from django.contrib import admin
from django.urls import path, include
from user.urls import userRouter
from products.urls import productRouter

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include(userRouter.urls)),
    path('', include(productRouter.urls)),
    
    path('',include('user.urls')),
    path('',include('products.urls')),
]
