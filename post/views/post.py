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

            return Response({ "error_message": 'Slug doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)

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
        post_type = int(request.GET.get('post_type'))
        data = []

        if post_type:
            if post_type == POST_TYPE.INTERNSHIP_POST_TYPE:
                data = InternshipSerializer(
                    Internship.objects.filter(is_verified=True, is_published=True).order_by('-created_at'),
                    context={'request': request},
                    many=True
                ).data

            elif post_type == POST_TYPE.PROJECT_POST_TYPE:
                data = ProjectSerializer(
                    Project.objects.filter(is_verified=True, is_published=True).order_by('-created_at'),
                    context={'request': request},
                    many=True
                ).data

            elif post_type == POST_TYPE.COMPETITION_POST_TYPE:
                data = CompetitionSerializer(
                    Competition.objects.filter(is_verified=True, is_published=True).order_by('-created_at'),
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
