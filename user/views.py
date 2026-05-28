from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import UserModel
from .serializers import RegisterCustomerSerializer, RegisterShopkeeperSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from .permissions import IsSelf
from .utils import send_reset_email

class RegisterCustomerViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = RegisterCustomerSerializer
    permission_classes = [AllowAny,]
    http_method_names = ['post',]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["role"] = UserModel.Role.CUSTOMER
        return context

class RegisterShopkeeperViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = RegisterShopkeeperSerializer
    permission_classes = [AllowAny,]
    http_method_names = ['post',]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["role"] = UserModel.Role.SHOPKEEPER
        return context
    
class UpdateRetrieveDeleteCostumerViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserModel.objects.all()
    serializer_class = RegisterCustomerSerializer
    permission_classes = [IsSelf,]

class UpdateRetrieveDeleteShopkeeperViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserModel.objects.all()
    serializer_class = RegisterShopkeeperSerializer
    permission_classes = [IsSelf,]

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny,]
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = UserModel.objects.filter(email=email).first()
            if user:
                send_reset_email(user)
            return Response({"message": "We will send you a link if you registered!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny,]
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)