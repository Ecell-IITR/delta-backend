from rest_framework import serializers

from common.field_choices import USER_FIELD_CHOICES

from users.serializers import PersonSerializer, SocialLinkSerializer
from users.models import Student

from utilities.serializers import BranchSerializer, SkillSerializer


class StudentSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)
    social_links = SocialLinkSerializer(many=True)
    skills = SkillSerializer(many=True)
    branch = BranchSerializer()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = '__all__'

    def get_followers_count(self, obj):
        return obj.person.action_on_person.filter(action=USER_FIELD_CHOICES.FOLLOW).count()
    
    def get_following_count(self, obj):
        return obj.person.action_by_person.filter(action=USER_FIELD_CHOICES.FOLLOW).count()

class StudentMinimumSerializer(serializers.ModelSerializer):
    person = PersonSerializer()

    class Meta:
        model = Student
        fields = ('person', 'first_name', 'last_name', 'enrollment_number')


class StudentMinInfoSerializer(serializers.ModelSerializer):
    is_follow = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = ('person', 'first_name', 'last_name', 'enrollment_number', 'is_follow', 'followers_count')
    
    def get_is_follow(self, obj):
        person = self.context.get('person') or None
        return obj.person.action_on_person.filter(
                action_by_person=person, action=USER_FIELD_CHOICES.FOLLOW).exists()
  
    def get_followers_count(self, obj):
        return obj.person.action_on_person.filter(action=USER_FIELD_CHOICES.FOLLOW).count()


class StudentDataSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)
    skill= SkillSerializer(many=True)
    class Meta:
        model = Student
        # fields = '__all__'
        exclude = ('resume', 'phone_number')