from rest_framework import serializers
from users.serializers import PersonSerializer
from users.models import Company


class CompanySerializer(serializers.ModelSerializer):
    person = PersonSerializer(
        read_only=True
    )

    class Meta:
        model = Company
        fields = '__all__'
