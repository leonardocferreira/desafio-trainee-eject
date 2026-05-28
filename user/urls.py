from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterCustomerViewSet, RegisterShopkeeperViewSet, ForgotPasswordView, ResetPasswordView, UpdateRetrieveDeleteCostumerViewSet, UpdateRetrieveDeleteShopkeeperViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('auth/register', RegisterCustomerViewSet, basename='user')
router.register('auth/shopkeeper', RegisterShopkeeperViewSet, basename='shopkeeper')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('auth/register/<int:pk>', UpdateRetrieveDeleteCostumerViewSet.as_view(), name='customer-detail'),
    path('auth/shopkeeper/<int:pk>', UpdateRetrieveDeleteShopkeeperViewSet.as_view(), name='shopkeeper-detail'),
    
    path('auth/forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('auth/reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]