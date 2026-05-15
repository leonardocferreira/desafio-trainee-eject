from rest_framework import serializers
from .models import UserModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True},
            'id': {'read_only': True},
        }
        fields = [
            'id',
            'name',
            'password',
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

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = UserModel.objects.create_user(password=password, **validated_data)
        return user