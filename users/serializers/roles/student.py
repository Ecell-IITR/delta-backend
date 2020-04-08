from rest_framework import serializers
from users.serializers import PersonSerializer, SocialLinkSerializer
from users.models import Student


class StudentSerializer(serializers.ModelSerializer):
    person = PersonSerializer(
        read_only=True
    )
    social_links = SocialLinkSerializer(many=True)

    class Meta:
        model = Student
        fields = '__all__'
