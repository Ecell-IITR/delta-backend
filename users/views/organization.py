from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from users.constants import GET_ROLE_TYPE
from users.serializers import CompanySerializer
from users.models import Company


class OrganizationList(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CompanySerializer

    def get_queryset(self, *args, **kwargs):
        list_type = self.request.GET.get('list_type')
        if list_type == 'all':
            queryset = Company.objects.all()
        else:
            queryset = []
        return queryset
