from rest_framework import serializers
from users.serializers import PersonSerializer, SocialLinkSerializer
from users.models import Student

from utilities.serializers import BranchSerializer, SkillSerializer


class StudentSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)
    social_links = SocialLinkSerializer(many=True)
    skills = SkillSerializer(many=True)
    branch = BranchSerializer()
    
    class Meta:
        model = Student
        fields = '__all__'
