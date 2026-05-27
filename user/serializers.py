import re
from rest_framework import serializers
from .models import UserModel

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

    def validate_email(self, value):
        if UserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.") 
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('password_confirm', None)
        role = validated_data.get('role', UserModel.Role.CUSTOMER)
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
    
    def validate_email(self, value):
        if UserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.") 
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('password_confirm', None)
        role = validated_data.get('role', UserModel.Role.SHOPKEEPER)
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
