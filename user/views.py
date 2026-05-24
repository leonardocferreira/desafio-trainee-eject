from django.shortcuts import render
from rest_framework import viewsets
from .serializers import RegisterSerializer
from .models import UserModel
from rest_framework.permissions import AllowAny

class RegisterViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]