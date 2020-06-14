from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import generics

from post.constants import POST_TYPE
from post.serializers import (
    CompetitionSerializer,
    InternshipSerializer,
    ProjectSerializer
)
from post.models import (
    Project,
    Competition,
    Internship,
    AppliedPostEntries
)
from post.permissions import IsStudent


class PostBaseView(views.APIView):
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        user = request.user

        if user.student_profile:
            user_profile = user.student_profile
        elif user.company_profile:
            user_profile = user.company_profile

        request.user_profile = user_profile


class PostViewSet(PostBaseView, viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, ]
    lookup_field = 'slug'

    def get_queryset(self):
        slug = self.kwargs['slug']

        if self.action in ['retrieve', 'update']:
            if Internship.objects.filter(slug=slug):
                return Internship.objects.filter(
                    slug=slug
                )
            if Project.objects.filter(slug=slug):
                return Project.objects.filter(
                    slug=slug
                )
            if Competition.objects.filter(slug=slug):
                return Competition.objects.filter(
                    slug=slug
                )

            return Response({"error_message": 'Slug doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        slug = self.kwargs['slug']

        if self.action in ['retrieve', 'update']:

            if Internship.objects.filter(slug=slug):
                return InternshipSerializer

            if Project.objects.filter(slug=slug):
                return ProjectSerializer

            if Competition.objects.filter(slug=slug):
                return CompetitionSerializer

            return Response(
                {
                    "error_message": 'Slug doesn\'t exists'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def list(self, request, *args, **kwargs):
        post_type = request.GET.get('post_type') or None
        my_post = request.GET.get('my_post') or False
        expired_post = request.GET.get('expired_post') or False
        unpublished_post = request.GET.get('unpublished_post') or False
        bookmark = request.GET.get('bookmark') or False
        applied_posts = request.GET.get('applied_posts') or False
        duration_value = request.GET.get('duration_value') or None
        duration_unit = request.GET.get('duration_unit') or None
        stipend_ll = request.GET.get('stipend_ll') or None
        stipend_ul = request.GET.get('stipend_ul') or None
        tag_hash = request.GET.getlist('tag_hash') or None
        location = request.GET.get('location') or None
        skill_slug = request.GET.getlist('skill_slug') or None
        now = timezone.now()

        if (duration_unit and duration_value is None) or (duration_unit is None and duration_value):
            return Response({"error_message": 'Duration param doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)
        data = []

        if post_type:
            if int(post_type) == POST_TYPE.INTERNSHIP_POST_TYPE:
                internships_queryset = Internship.objects.filter(is_verified=True, is_published=True,
                                                                 post_expiry_date__gte=now)\
                                                .order_by('-created_at')
                if my_post:
                    internships_queryset = Internship.objects.filter(user=request.user, is_published=True,
                                                                     post_expiry_date__gte=now)\
                                                .order_by('-created_at')
                if expired_post:
                    internships_queryset = Internship.objects.filter(post_expiry_date__lte=now)\
                                                .order_by('-created_at')
                if unpublished_post:
                    internships_queryset = Internship.objects.filter(is_published=False, post_expiry_date__gte=now)\
                                                .order_by('-created_at')
                if bookmark:
                    internships_queryset = internships_queryset.filter(bookmarks__person=request.user)
                if applied_posts:
                    post_ids = AppliedPostEntries.objects.filter(user_object_id=request.user_profile.id)\
                                        .values_list('post_object_id', flat=True).distinct()
                    internships_queryset = internships_queryset.filter(id__in=post_ids)
                if stipend_ll:
                    internships_queryset = internships_queryset.filter(stipend__gte=int(stipend_ll))
                if stipend_ul:
                    internships_queryset = internships_queryset.filter(stipend__lte=int(stipend_ul))
                if duration_value and duration_unit:
                    internships_queryset = internships_queryset.filter(duration_unit=duration_unit,
                                                                       duration_value=duration_value)
                if location:
                    internships_queryset = internships_queryset.filter(location__slug=location)
                if tag_hash:
                    internships_queryset = internships_queryset.filter(tags__hash__in=tag_hash)
                if skill_slug:
                    internships_queryset = internships_queryset.filter(required_skills__slug__in=skill_slug)

                data = InternshipSerializer(
                    internships_queryset,
                    context={'request': request},
                    many=True
                ).data

            elif int(post_type) == POST_TYPE.PROJECT_POST_TYPE:
                data = ProjectSerializer(
                    Project.objects.filter(is_verified=True, is_published=True, post_expiry_date__gte=now)
                        .order_by('-created_at'),
                    context={'request': request},
                    many=True
                ).data

            elif int(post_type) == POST_TYPE.COMPETITION_POST_TYPE:
                data = CompetitionSerializer(
                    Competition.objects.filter(is_verified=True, is_published=True, post_expiry_date__gte=now)
                        .order_by('-created_at'),
                    context={'request': request},
                    many=True
                ).data

            return Response(data, status=status.HTTP_200_OK)
        return Response({"error_message": 'Post type param doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)


class CreatePost(generics.CreateAPIView):

    permission_classes = [IsAuthenticated, ]

    def get_serializer_context(self):
        return {"user": self.request.user}

    def get_serializer_class(self):
        post_type = self.request.data.get('post_type')

        if post_type == 'internship':
            return InternshipSerializer
        elif post_type == 'project':
            return ProjectSerializer
        elif post_type == 'competition':
            return CompetitionSerializer

        return None

    def post(self, request, *args, **kwargs):
        if not self.request.data.get('post_type'):
            return Response({'error_message':'post_type field required'}, status=status.HTTP_400_BAD_REQUEST)

        if not self.request.data.get('post_type') in ['internship', 'project', 'competition']:
            return Response({'error_message': 'post_type field value is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class ApplyPostView(PostBaseView):
    permission_classes = [IsAuthenticated, IsStudent]

    @staticmethod
    def check_post_object(slug):
        if Internship.objects.filter(slug=slug).exists():
            return Internship.objects.get(slug=slug)

        elif Project.objects.filter(slug=slug).exists():
            return Project.objects.get(slug=slug)

        elif Competition.objects.filter(slug=slug).exists():
            return Competition.objects.get(slug=slug)

        return None

    def post(self, request, *args, **kwargs):
        user_profile = request.user_profile
        post_slug = self.kwargs['slug']

        post = self.check_post_object(post_slug)

        if post:
            if post.applied_post_entries.filter(user_object_id=user_profile.id).exists():
                return Response({"error_message": 'Already applied to the post!'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                AppliedPostEntries.objects.create(user=user_profile, post=post)
                return Response(status=status.HTTP_200_OK)
            except:
                return Response({"error_message": 'Unable to apply'}, status=status.HTTP_403_FORBIDDEN)

        return Response({"error_message": 'Slug doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)
