from rest_framework import serializers

from users.models import Person


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ("username", "password")
