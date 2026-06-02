from .models import Contact
from rest_framework import serializers
from .validators import valid_phone_number, valid_name

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            'id',
            'name',
            'phone_number',
            'email',
            'subject',
            'message',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

        def validate(self, attrs):
            if not valid_phone_number(attrs['phone_number']):
                raise serializers.ValidationError({'phone_number': 'Phone number must have this format: "99 9 9999-9999".'})