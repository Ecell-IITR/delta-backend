from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets

from users.constants import GET_ROLE_TYPE

from users.serializers import (
    StudentSerializer,
    CompanySerializer,
    PersonSerializer
)

from users.models import (
    Student,
    Person,
    Company
)


class WhoAmIViewSet(viewsets.ModelViewSet):
    """
    This view shows some personal information of the currently logged in person
    """

    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        """
        This function decides the queryset according to the type of
        user
        :return: the queryset
        """
        person = self.request.user
        role_type = self.request.user.role_type

        if role_type == GET_ROLE_TYPE.STUDENT:
            queryset = Student.objects.get(person=person)
        elif role_type == GET_ROLE_TYPE.COMPANY:
            queryset = Company.objects.get(person=person)
        else:
            queryset = Person.objects.all(person=person)

        return queryset

    def get_serializer_class(self):
        """
        This function decides the serializer class according to the type of
        user
        :return: the serializer class
        """

        if self.request.user.role_type == GET_ROLE_TYPE.STUDENT:
            return StudentSerializer
        elif self.request.user.role_type == GET_ROLE_TYPE.COMPANY:
            return CompanySerializer
        else:
            return PersonSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(queryset)
        if serializer.is_valid:
            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(
            queryset,
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True
        )
        self.perform_update(
            serializer
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
