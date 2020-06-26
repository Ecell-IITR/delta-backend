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

    def to_representation(self, instance):
        response = super(PersonSerializer, self).to_representation(instance)
        if instance.profile_image:
            response['profile_image'] = instance.profile_image.url
        return response