import datetime

from django.utils import timezone
from django.contrib.auth.models import update_last_login

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from users.models import (
    Student,
    Company,
    Person
)
from users.constants import GET_ROLE_TYPE


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.SerializerMethodField(
        read_only=True
    )

    class Meta:
        model = Person
        exclude = ('last_login', 'is_superuser', 'date_joined', 'created_at', 'updated_at', 'is_active', 'is_admin',
                    'groups', 'user_permissions',)

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
        token = Token.objects.create(user=user)
        return token.key

    def validate(self, data):
        check = data.get('role_type') or None
        if check is None:
            raise serializers.ValidationError("Role must be defined!")
        return data

    def create(self, validated_data):
 
        if validated_data.get('role_type') == GET_ROLE_TYPE.STUDENT:
            person = Person.objects.create(
                username=validated_data.get('username'),
                email=validated_data.get('email'),
                role_type=GET_ROLE_TYPE.STUDENT
            )
            student = Student.objects.create(
                person=person
            )
            student.save()
        elif validated_data.get('role_type') == GET_ROLE_TYPE.COMPANY:
            person = Person.objects.create(
                username=validated_data.get('username'),
                email=validated_data.get('email'),
                role_type=GET_ROLE_TYPE.COMPANY
            )
            company = Company.objects.create(
                person=person
            )
            company.save()

        person.set_password(validated_data.get('password'))
        person.save()

        update_last_login(None, person)
        return person
