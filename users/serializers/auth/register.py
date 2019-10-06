import datetime

from django.utils import timezone

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from users.models import (
    Student,
    Company,
    Person
)
from users.utils import jwt_response_payload_handler

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
JWT_RESPONSE_PAYLOAD_HANDLER = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

expire_delta = api_settings.JWT_REFRESH_EXPIRATION_DELTA


class RegisterSerializer(serializers.ModelSerializer):

    # username = serializers.CharField()

    # email = serializers.CharField()
    # is_student = serializers.Boolea

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    token = serializers.SerializerMethodField(
        read_only=True
    )

    expires = serializers.SerializerMethodField(
        read_only=True
    )

    message = serializers.SerializerMethodField(
        read_only=True
    )

    class Meta:
        model = Person
        fields = '__all__'

    def get_message(self, *args, **kwargs):
        '''
        Return the successful registeration message
        '''
        return 'Thank You for registering pls verify your email'

    def validate_email(self, value):
        email = Person.objects.filter(email__iexact=value)
        if email.exists():
            raise serializers.ValidationError('User email already registered')
        return value

    def validate_username(self, value):
        username = Person.objects.filter(username__iexact=value)
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
        person = Person.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
        )
        if validated_data.get('is_student'):
            person.is_student = True
            student = Student.objects.create(
                person=person
            )
            student.save()
        elif validated_data.get('is_company'):
            person.is_company = True
            company = Company.objects.create(
                person=person
            )
            company.save()
        person.set_password(validated_data.get('password'))
        person.save()
        return person
