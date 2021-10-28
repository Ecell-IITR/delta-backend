from rest_framework import serializers
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers.roles.student import StudentDataSerializer
from users.models import Student
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class StudentAPI(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        id = pk
        stu = Student.objects.get(id =id)
        serializer = StudentDataSerializer(stu)
        return Response(serializer.data, status=status.HTTP_200_OK)
                
