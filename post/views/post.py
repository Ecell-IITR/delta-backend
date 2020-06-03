from django.utils import timezone

from rest_framework import status
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
    Internship
)


class PostViewSet(viewsets.ModelViewSet):

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
        duration_value = request.GET.get('duration_value') or None
        duration_unit = request.GET.get('duration_unit') or None
        stipend_ll = request.GET.get('stipend_ll') or None
        stipend_ul = request.GET.get('stipend_ul') or None
        tag_hashes = request.GET.get('tag_hashes') or None
        location = request.GET.get('location') or None
        skill_slugs = request.GET.get('skill_slugs') or None
        now = timezone.now()

        if (duration_unit and duration_value is None) or (duration_unit is None and duration_value):
            return Response({"error_message": 'Duration param doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)
        data = []

        if post_type:
            if int(post_type) == POST_TYPE.INTERNSHIP_POST_TYPE:
                internships_queryset = Internship.objects.filter(is_verified=True, is_published=True,
                                                                 post_expiry_date__gte=now)\
                                                .order_by('-created_at')

                if stipend_ll:
                    internships_queryset = internships_queryset.filter(stipend__gte=int(stipend_ll))
                if stipend_ul:
                    internships_queryset = internships_queryset.filter(stipend__lte=int(stipend_ul))
                if duration_value and duration_unit:
                    internships_queryset = internships_queryset.filter(duration_unit=duration_unit,
                                                                       duration_value=duration_value)
                if location:
                    internships_queryset = internships_queryset.filter(location__slug=location)
                if tag_hashes:
                    internships_queryset = internships_queryset.filter(tags__hash__in=tag_hashes)
                if skill_slugs:
                    internships_queryset = internships_queryset.filter(required_skills__slug__in=skill_slugs)

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
