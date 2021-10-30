from rest_framework import serializers

from common.field_choices import USER_FIELD_CHOICES

from users.serializers import PersonSerializer
from users.models import Company


class CompanySerializer(serializers.ModelSerializer):
    person = PersonSerializer(
        read_only=True
    )

    class Meta:
        model = Company
        fields = '__all__'


class CompanyMinimumSerializer(serializers.ModelSerializer):
    person = PersonSerializer(
        read_only=True
    )
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ('person', 'company_domain', 'phone_number', 'followers_count')
    
    @staticmethod
    def get_followers_count(obj):
        return obj.person.action_on_person.filter(action=USER_FIELD_CHOICES.FOLLOW).count()


class CompanyDataSerializer(serializers.ModelSerializer):
    person = PersonSerializer(
        read_only=True
    )
    
    class Meta:
        model = Company
        fields = '__all__'