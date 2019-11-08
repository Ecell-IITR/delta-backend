import datetime

from django.utils import timezone

from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings


from users.utils import jwt_response_payload_handler

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
JWT_RESPONSE_PAYLOAD_HANDLER = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

expire_delta = api_settings.JWT_REFRESH_EXPIRATION_DELTA


class LoginSerializer(serializers.Serializer):

    id = serializers.IntegerField(
        read_only=True
    )

    username = serializers.CharField(
        max_length=255
    )

    email = serializers.CharField()

    password = serializers.CharField(
        max_length=128,
        write_only=True
    )

    token = serializers.CharField(
        max_length=255,
        read_only=True
    )

    def validate(self, data):

        user = authenticate(
            username=data.get('username'),
            password=data.get('password')
        )

        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password was not found.'
            )

        # if not user.is_active:
        #     raise serializers.ValidationError(
        #         'This user has been deactivated.'
        #     )
        payload = JWT_PAYLOAD_HANDLER(user)
        token = JWT_ENCODE_HANDLER(payload)
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'token': token
        }
