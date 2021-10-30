from django.shortcuts import render, get_object_or_404

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.constants import GET_ROLE_TYPE
from users.models import Student, Company
from utilities.serializers import SkillSerializer, LocationSerializer, TagSerializer, TypeSerializer
from utilities.models import Skill, Tag, Location,Type


class SkillBaseView(APIView):
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        user = request.user
        skill_slug = kwargs.get('slug')

        if skill_slug:
            try:
                skill = get_object_or_404(Skill, slug=skill_slug)
            except:
                return Response({"error_message": 'Slug doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)
            request.skill = skill

        if user.student_profile:
            user_profile = user.student_profile
        elif user.company_profile:
            user_profile = user.company_profile

        request.user_profile = user_profile


class SkillsAPIView(SkillBaseView, generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    pagination_class = None
    serializer_class = SkillSerializer

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        user_profile = self.request.user_profile
        
        user_skills_queryset = user_profile.skills.all()
        total_skills_queryset = Skill.objects.all()
        return total_skills_queryset.difference(user_skills_queryset)


class SkillAddAPI(SkillBaseView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        user = request.user
        skill = request.skill
        user_profile = request.user_profile

        if skill in user_profile.skills.all():
            return Response({"error_message": 'Skill already added!'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_profile.skills.add(skill)
        user_profile.save()

        return Response(status=status.HTTP_202_ACCEPTED)


class SkillRemoveAPI(SkillBaseView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        user = request.user
        skill = request.skill
        user_profile = request.user_profile

        if not skill in user_profile.skills.all():
            return Response({"error_message": 'Skill already removed!'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_profile.skills.remove(skill)
        user_profile.save()

        return Response(status=status.HTTP_202_ACCEPTED)

class SkillRemoveAllAPI(SkillBaseView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        user = request.user
        user_profile = request.user_profile
        
        user_profile.skills.clear()
        user_profile.save()

        return Response(status=status.HTTP_202_ACCEPTED)

# class TagsAutoComplete(autocomplete.Select2QuerySetView):

#     def get_queryset(self):
#         print('here')
#         qs = Tag.objects.all().order_by('title')
#         if self.q:
#             qs = qs.filter(title__icontains=self.q)
#         return qs


class LocationsListAPI(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    pagination_class = None
    serializer_class = LocationSerializer
    queryset = Location.objects.all()


class TagsListAPI(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    pagination_class = None
    serializer_class = TagSerializer
    queryset = Tag.objects.all()











class TypeSkillsAPIView(SkillBaseView, generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    pagination_class = None
    serializer_class = TypeSerializer

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        user_profile = self.request.user_profile
        
        user_skills_queryset = user_profile.type.all()
        total_skills_queryset = Type.objects.all()
        return total_skills_queryset.difference(user_skills_queryset)