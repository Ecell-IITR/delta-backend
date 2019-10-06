from rest_framework import serializers
from users.serializers import PersonSerializer
from users.models import Student


class StudentSerializer(serializers.ModelSerializer):
    person = PersonSerializer(
        read_only=True
    )

    class Meta:
        model = Student
        fields = '__all__'
