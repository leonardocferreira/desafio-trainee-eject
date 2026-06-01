from rest_framework import serializers
from .models import UserModel
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .validators import valid_cpf, valid_cep, valid_phone_number, valid_name, password_match

class RegisterCustomerSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)    
    
    class Meta:
        model = UserModel
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
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True},
            'address': {'required': True},
            'birth_date': {'required': True},
            'phone_number': {'required': True},
            'cpf': {'required': True},
            'cep': {'required': True},
        }
        read_only_fields = ['id', 'role',]

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        if not valid_cpf(attrs.get('cpf')):
            raise serializers.ValidationError({'cpf': 'CPF must have this format: "999.999.999-99"'})
        if not valid_cep(attrs.get('cep')):
            raise serializers.ValidationError({'cep': 'CEP must have this format: "99999-999"'})
        if not valid_phone_number(attrs.get('phone_number')):
            raise serializers.ValidationError({'phone_number': 'Phone number must have this format: "99 9 9999-9999"'})
        if not valid_name(attrs.get('name')):
            raise serializers.ValidationError({'name': 'Name must have at least 2 characters and only letters.'})
        if not password_match(attrs.get('password'), attrs.get('password_confirm')):
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
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
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True},
        }
        read_only_fields = ['id', 'role',]
    
    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        if not password_match(attrs.get('password'), attrs.get('password_confirm')):
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
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
        if not password_match(data.get('new_password'), data.get('confirm_password')):
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        
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