from rest_framework import serializers

from users.serializers import PersonSerializer, StudentMinimumSerializer, CompanyMinimumSerializer

from post.models import Internship, AppliedPostEntries
from post.constants import POST_TYPE

from utilities.serializers import TagSerializer


class InternshipSerializer(serializers.ModelSerializer):

    user_min_profile = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    post_type = serializers.SerializerMethodField()
    is_bookmark = serializers.SerializerMethodField()
    applicants_count = serializers.SerializerMethodField()

    class Meta:
        model = Internship
        exclude = ('bookmarks', )
    
    @staticmethod
    def get_post_type(obj):
        return POST_TYPE.INTERNSHIP_POST_TYPE

    def get_is_bookmark(self, obj):
        person = self.context.get('user', None)
        starred_posts = obj.bookmarks.all()
        return starred_posts.filter(person=person).exists()
    
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

    @staticmethod    
    def get_applicants_count(obj):
        return obj.applied_post_entries.count()