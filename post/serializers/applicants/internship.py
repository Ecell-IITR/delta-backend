from rest_framework import serializers
from post.models.post_roles.internship import Internship
from users.serializers import StudentMinimumSerializer, StudentSerializer, CompanyMinimumSerializer
from post.models import AppliedPostEntries


class ApplicantsInternSerializers(serializers.ModelSerializer):

    applicant_profile = serializers.SerializerMethodField()

    class Meta:
        model = AppliedPostEntries
        fields = ['applicant_profile', ]

    @staticmethod
    def get_applicant_profile(obj):
        person = obj.user

        try:
            return StudentSerializer(person).data
        except:
            return None


class InternMinimumSerializer(serializers.ModelSerializer):

    author_profile = serializers.SerializerMethodField()
    applicants_count = serializers.SerializerMethodField()
    applicants = serializers.SerializerMethodField()

    class Meta:
        model = Internship
        fields = ['id', 'author_profile', 'slug', 'title', 'description', 'location',
                  'duration_value', 'stipend', 'is_published', 'is_verified', 'applicants_count', "applicants"]

    @staticmethod
    def get_applicants_count(obj):
        return obj.applied_post_entries.count()

    @staticmethod
    def get_applicants(obj):
        person = obj.applied_post_entries.all()
        try:
            return ApplicantsInternSerializers(person, many=True).data
        except:
            return None

    @staticmethod
    def get_author_profile(obj):
        person = obj.user
        try:
            user_profile = person.student_profile
            return StudentMinimumSerializer(user_profile).data
        except:
            user_profile = person.company_profile
            return CompanyMinimumSerializer(user_profile).data