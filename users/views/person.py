from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

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


class BasicUser(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

    def get_object(self):
        return get_object_or_404(Person, pk=self.request.user.pk)


class SelfProfile(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        person = self.request.user
        role_type = self.request.user.role_type

        if role_type == GET_ROLE_TYPE.STUDENT:
            queryset = Student.objects.get(person=person)
        elif role_type == GET_ROLE_TYPE.COMPANY:
            queryset = Company.objects.get(person=person)
        else:
            queryset = None
        return queryset

    def get_serializer_class(self):
        if self.request.user.role_type == GET_ROLE_TYPE.STUDENT:
            return StudentSerializer
        elif self.request.user.role_type == GET_ROLE_TYPE.COMPANY:
            return CompanySerializer
        else:
            return None

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(queryset)
        if serializer.is_valid:
            return Response(serializer.data, status=status.HTTP_200_OK)
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
