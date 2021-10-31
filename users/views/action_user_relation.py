from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from common.field_choices import get_opposite_action
from users.serializers import ActionUserRelationSerializer
from users.models import ActionUserRelation
from users.models import Person


class ActionRelationBaseView(APIView):
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        user = request.user
        action = kwargs.get("action_key")
        action_on_person_username = kwargs.get("username")

        try:
            action_on_person = get_object_or_404(
                Person, username=action_on_person_username
            )
        except:
            return Response(
                {"error_message": "Username doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.student_profile:
            user_profile = user.student_profile
        elif user.company_profile:
            user_profile = user.company_profile

        request.action = action
        request.user_profile = user_profile
        request.action_on_person = action_on_person


class ActionView(ActionRelationBaseView, APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ActionUserRelationSerializer

    @staticmethod
    def post(request, *args, **kwargs):
        user = request.user
        action = request.action
        action_on_person = request.action_on_person

        check_action_user_relation = ActionUserRelation.objects.filter(
            action_on_person=action_on_person, action_by_person=user, action=action
        )
        if check_action_user_relation.exists():
            return Response(
                {"error_message": "Relation already exists!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            check_opposite_action_user_relation = user.action_by_person.get(
                action_on_person=action_on_person, action=get_opposite_action(action)
            )
            check_opposite_action_user_relation.action = action
            check_opposite_action_user_relation.save()

            return Response(status=status.HTTP_201_CREATED)
        except:
            pass

        try:
            ActionUserRelation.objects.create(
                action_on_person=action_on_person, action_by_person=user, action=action
            )
        except:
            return Response(
                {"error_message": "Username or action key invalid!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_201_CREATED)
