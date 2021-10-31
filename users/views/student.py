from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers.roles.student import StudentDataSerializer
from users.models import Student
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class StudentAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentDataSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response(
                {"error_message": "id doesn't exist"}, status=status.HTTP_404_NOT_FOUND
            )
