from django.shortcuts import render
from .models import Contact
from .serializers import ContactSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .utils import send_contact_email

class ContactView(APIView):
    permission_classes = [AllowAny,]
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save()    
            send_contact_email(contact)
            return Response({'message': 'Email sent successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

