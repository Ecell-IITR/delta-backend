from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from utilities.serializers import SkillSerializer
from utilities.models import Skill


class SkillsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    pagination_class = None
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()