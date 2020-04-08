import datetime

from django.utils import timezone

from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.authtoken.models import Token


class LoginSerializer(serializers.Serializer):

    id = serializers.IntegerField(
        read_only=True
    )

    username = serializers.CharField(
        max_length=255
    )

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
        token = Token.objects.get_or_create(user=user)
        return {
            'id': user.id,
            'username': user.username,
            'token': token
        }
