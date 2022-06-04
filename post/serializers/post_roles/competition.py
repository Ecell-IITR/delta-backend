from rest_framework import serializers

from users.serializers import PersonSerializer
from users.serializers import StudentMinimumSerializer, CompanyMinimumSerializer

from post.models import Competition
from post.constants import POST_TYPE

from utilities.serializers import TagSerializer, SkillSerializer, LocationSerializer


class CompetitionSerializer(serializers.ModelSerializer):

    user = PersonSerializer(read_only=True)
    user_min_profile = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    post_type = serializers.SerializerMethodField()
    is_bookmark = serializers.SerializerMethodField()
    location = LocationSerializer()
    required_skills = SkillSerializer(many=True)

    class Meta:
        model = Competition
        exclude = ('bookmarks', )
    
    @staticmethod
    def get_post_type(obj):
        return POST_TYPE.COMPETITION_POST_TYPE
    
    @staticmethod
    def get_user_min_profile(obj):
        person = obj.user
        try:
            user_profile = person.student_profile
            return StudentMinimumSerializer(user_profile).data
        except: 
            pass
        try:
            user_profile = person.company_profile
            return CompanyMinimumSerializer(user_profile).data
        except: 
            pass
        return {}

    def get_is_bookmark(self, obj):
        person = self.context['request'].user
        starred_posts = obj.bookmarks.all()
        return starred_posts.filter(person=person).exists()
