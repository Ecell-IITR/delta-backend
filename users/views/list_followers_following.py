from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from common.field_choices import USER_FIELD_CHOICES
from common.pagination import AllListsPagination

from users.constants import GET_ROLE_TYPE
from users.models import Person, Student, Company
from users.models import ActionUserRelation
from users.serializers import OrganizationListSerializer, StudentMinInfoSerializer


class BaseListView(APIView):
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        user = request.user

        if user.student_profile:
            user_profile = user.student_profile
        elif user.company_profile:
            user_profile = user.company_profile

        request.user_profile = user_profile


class FollowersList(BaseListView, generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def list(request, *args, **kwargs):
        user = request.user

        student_queryset = user.action_on_person.filter(
            action_by_person__role_type=GET_ROLE_TYPE.STUDENT,
            action=USER_FIELD_CHOICES.FOLLOW,
        ).values_list("action_by_person__username", flat=True)
        student_data = StudentMinInfoSerializer(
            Student.objects.filter(person__username__in=student_queryset),
            context={"person": request.user},
            many=True,
        ).data

        company_queryset = user.action_on_person.filter(
            action_by_person__role_type=GET_ROLE_TYPE.COMPANY,
            action=USER_FIELD_CHOICES.FOLLOW,
        ).values_list("action_by_person__username", flat=True)
        company_data = OrganizationListSerializer(
            Company.objects.filter(person__username__in=company_queryset),
            context={"person": request.user},
            many=True,
        ).data

        return Response(student_data + company_data, status=status.HTTP_200_OK)


class FollowingList(BaseListView, generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        student_queryset = user.action_by_person.filter(
            action_on_person__role_type=GET_ROLE_TYPE.STUDENT,
            action=USER_FIELD_CHOICES.FOLLOW,
        ).values_list("action_on_person__username", flat=True)
        student_data = StudentMinInfoSerializer(
            Student.objects.filter(person__username__in=student_queryset),
            context={"person": request.user},
            many=True,
        ).data

        company_queryset = user.action_by_person.filter(
            action_on_person__role_type=GET_ROLE_TYPE.COMPANY,
            action=USER_FIELD_CHOICES.FOLLOW,
        ).values_list("action_on_person__username", flat=True)
        company_data = OrganizationListSerializer(
            Company.objects.filter(person__username__in=company_queryset),
            context={"person": request.user},
            many=True,
        ).data

        return Response(student_data + company_data, status=status.HTTP_200_OK)
