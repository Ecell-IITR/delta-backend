from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from utilities.serializers import SkillSerializer
from utilities.models import Skill, Tag


class SkillsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    pagination_class = None
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()


# class TagsAutoComplete(autocomplete.Select2QuerySetView):

#     def get_queryset(self):
#         print('here')
#         qs = Tag.objects.all().order_by('title')
#         if self.q:
#             qs = qs.filter(title__icontains=self.q)
#         return qs

