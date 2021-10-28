from typing_extensions import ParamSpecKwargs
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from users import serializers
from users.models.roles.company import Company
from users.serializers.roles.company import CompanyDataSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated




class CompanyAPI(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None, format=None):
        id = pk
        Comp = Company.objects.get(id=id)
        serializer = CompanyDataSerializer(Comp)
        return Response(serializer.data)
