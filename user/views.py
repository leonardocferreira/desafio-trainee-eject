from django.shortcuts import render
from rest_framework import viewsets
from .serializers import RegisterCustomerSerializer, RegisterShopkeeperSerializer
from .models import UserModel
from rest_framework.permissions import AllowAny

class RegisterCustomerViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = RegisterCustomerSerializer
    permission_classes = [AllowAny,]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["role"] = UserModel.Role.CUSTOMER
        return context

class RegisterShopkeeperViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = RegisterShopkeeperSerializer
    permission_classes = [AllowAny,]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["role"] = UserModel.Role.SHOPKEEPER
        return context