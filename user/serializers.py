import re
from rest_framework import serializers
from .models import UserModel
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

class RegisterCustomerSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)    
    
    class Meta:
        model = UserModel
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True},
            'address': {'required': True},
            'birth_date': {'required': True},
            'phone_number': {'required': True},
            'cpf': {'required': True},
            'cep': {'required': True},
        }
        fields = [
            'id',
            'name',
            'password',
            'password_confirm',
            'email',
            'address',
            'birth_date',
            'phone_number',
            'cpf',
            'cep',
            'role',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'role',]

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords do not match.')
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('password_confirm', None)
        role = validated_data.pop('role', UserModel.Role.CUSTOMER)
        user = UserModel.objects.create_user(password=password,role=role,**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('password_confirm', None)
        if password:
            instance.set_password(password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class RegisterShopkeeperSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)    
    
    class Meta:
        model = UserModel
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True},
        }
        read_only_fields = ['id', 'role',]
        fields = [
            'id',
            'name',
            'password',
            'password_confirm',
            'email',
            'role',
            'created_at',
            'updated_at',
        ]
    
    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords do not match.')
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('password_confirm', None)
        role = validated_data.pop('role', UserModel.Role.SHOPKEEPER)
        user = UserModel.objects.create_user(password=password,role=role,**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('password_confirm', None)
        
        if password:
            instance.set_password(password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save() 
        return instance

class ForgotPasswordSerializer(serializers.Serializer):
    # sem validate_email por questões de segurança, para não expor se um email está registrado ou não
    email = serializers.EmailField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
    
    def validate(self, data):
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        
        if new_password != confirm_password:
            raise serializers.ValidationError('Passwords do not match.')
        
        try:
            uid = urlsafe_base64_decode(data['uidb64']).decode()
            user = UserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            raise serializers.ValidationError('Token or UID is invalid.')
        
        if not default_token_generator.check_token(user, data['token']):
            raise serializers.ValidationError('Invalid token.')
        
        data['user'] = user
        return data
    
    def save(self):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user