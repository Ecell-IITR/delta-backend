from rest_framework import serializers

from users.models import Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            'id',
            'username',
            'email',
            'profile_image',
            'secondary_email',
            'role_type'
        ]
