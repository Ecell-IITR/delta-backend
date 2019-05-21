import datetime

from django.utils import timezone
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from users.models.user import User
from users.utils import jwt_response_payload_handler

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
JWT_RESPONSE_PAYLOAD_HANDLER = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

expire_delta = api_settings.JWT_REFRESH_EXPIRATION_DELTA


class PublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username'
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    expires = serializers.SerializerMethodField(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'password2',
            'token',
            'expires',
            'message',
            'company_domain'
        ]

    def get_message(self, *args, **kwargs):
        '''
        Return the successful registeration message
        '''
        return 'Thank You for registering pls verify your email'

    def validate_email(self, value):
        email = User.objects.filter(email__iexact=value)
        if email.exists():
            raise serializers.ValidationError('User email already registered')
        return value

    def validate_username(self, value):
        username = User.objects.filter(username__iexact=value)
        if username.exists():
            raise serializers.ValidationError('Username already registered ')
        return value

    def get_token(self, obj):
        user = obj
        payload = JWT_PAYLOAD_HANDLER(user)
        token = JWT_ENCODE_HANDLER(payload)
        return token

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords must match")
        return data

    def get_expires(self, obj):
        return timezone.now() + expire_delta - datetime.timedelta(seconds=200)

    def create(self, validated_data):
        if validated_data.get('company_domain') is not None:
            user = User.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            company_domain=validated_data.get('company_domain')
            )
        else:
            user = User.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email'))
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class EditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]
        read_only_fields = [
            'username',
        ]

    def validate_email(self, value):
        email = User.objects.filter(email__iexact=value)
        if self.instance:
            email = email.exclude(pk=self.instance.pk)
        if email.exists():
            raise serializers.ValidationError('User email already registered')
        return value

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data['email']
        password = data['password']

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        payload = JWT_PAYLOAD_HANDLER(user)
        token = JWT_ENCODE_HANDLER(payload)
        return {
            'id':user.id,
            'email': user.email,
            'username': user.username,
            'token': token
        }
