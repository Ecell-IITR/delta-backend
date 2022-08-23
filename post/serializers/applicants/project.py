from rest_framework import serializers
from post.models.post_roles import Project
from users.serializers import StudentMinimumSerializer, StudentSerializer, CompanyMinimumSerializer, PersonSerializer
from post.models import AppliedPostEntries
from users.constants import GET_ROLE_TYPE
from post.serializers.post_roles import ProjectSerializer


class ApplicantProjectSerializer(serializers.ModelSerializer):

    applicant_profile = serializers.SerializerMethodField()

    class Meta:
        model = AppliedPostEntries
        fields = ['applicant_profile']

    @staticmethod
    def get_applicant_profile(obj):
        person = obj.user
        try:
            return StudentSerializer(person).data
        except:
            return None


class ProjectMinimumSerializer(ProjectSerializer):

    author_profile = serializers.SerializerMethodField()
    applicants_count = serializers.SerializerMethodField()
    applicants = serializers.SerializerMethodField()


    @staticmethod
    def get_applicants_count(obj):
        return obj.applied_post_entries.count()

    @staticmethod
    def get_applicants(obj):
        person = obj.applied_post_entries.all()
        try:
            return ApplicantProjectSerializer(person, many=True).data
        except:
            return None

    @staticmethod
    def get_author_profile(obj):
        person = obj.user
        try:
            if person.role_type == GET_ROLE_TYPE.STUDENT:
                user_profile = person.student_profile
                return StudentMinimumSerializer(user_profile).data
            elif person.role_type == GET_ROLE_TYPE.COMPANY:
                user_profile = person.company_profile
                return CompanyMinimumSerializer(user_profile).data
            else:
                user_profile = person.person_profile
                return PersonSerializer(user_profile).data
        except:
            return None
