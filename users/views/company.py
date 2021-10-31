from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models.roles.company import Company
from users.serializers.roles.company import CompanyDataSerializer
from rest_framework import status





class CompanyAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None, format=None):
        try:
            company = Company.objects.get(id=pk)
            serializer = CompanyDataSerializer(company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({"error_message": 'id doesn\'t exist'}, status=status.HTTP_404_NOT_FOUND)



