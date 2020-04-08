import datetime

from django.utils import timezone

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from users.models import (
    Student,
    Company,
    Person
)


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length=8,
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
        token = Token.objects.create(user=user)
        return token

    def validate(self, data):
        check = data.get('is_student') or data.get('is_company') or False

        if check is not True:
            raise serializers.ValidationError("Role must be defined!")

        return data

    def get_expires(self, obj):
        return timezone.now() + expire_delta - datetime.timedelta(seconds=200)

    def create(self, validated_data):
        person = Person.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
        )
        if validated_data.get('is_student'):
            person.role = 'Student'
            student = Student.objects.create(
                person=person
            )
            student.save()
        elif validated_data.get('is_company'):
            person.role = 'Company'
            company = Company.objects.create(
                person=person
            )
            company.save()

        person.set_password(validated_data.get('password'))
        person.save()
        return person
