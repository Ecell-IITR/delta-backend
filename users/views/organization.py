from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from common.field_choices import USER_FIELD_CHOICES

from users.constants import GET_ROLE_TYPE
from users.serializers import OrganizationListSerializer
from users.models import Company


class OrganizationList(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = OrganizationListSerializer

    def get_serializer_context(self, *args, **kwargs):
        context = super(OrganizationList, self).get_serializer_context()
        context.update({'person': self.request.user})
        return context

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        list_type = self.request.GET.get('list_type')
        queryset = []
        if list_type == 'all':
            queryset = Company.objects.all()
        elif list_type == 'following-list':
            company_user_list = user.action_by_person.filter(action_on_person__role_type=GET_ROLE_TYPE.COMPANY, 
                action=USER_FIELD_CHOICES.FOLLOW).values_list('action_on_person__username', flat=True)
            queryset = Company.objects.filter(person__username__in=company_user_list)
        return queryset
