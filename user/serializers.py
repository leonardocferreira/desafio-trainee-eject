from rest_framework import serializers
from .models import UserModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        extra_kwargs = {
            'password': {'write_only': True},
        }
        fields = [
            'id',
            'name',
            'email',
            'address',
            'birth_date',
            'phone_number',
            'cpf',
            'cep',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']