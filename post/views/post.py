from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets

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
    """
    This view shows some personal information of the currently logged in person
    """

    permission_classes = [IsAuthenticated, ]
    lookup_field = 'slug'

    def get_queryset(self):
        """
        This function decides the queryset according to the type of
        post
        :return: the queryset
        """
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

            return Response(
                {
                    "error_message": 'Slug doesn\'t exists'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_serializer_class(self):
        """
        This function decides the serializer class according to the type of
        post
        :return: the serializer class
        """

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

        elif self.action in ['create']:
            data = self.request.data

            if data['internship']:
                return InternshipSerializer

            elif data['project']:
                return ProjectSerializer

            elif data['competition']:
                return CompetitionSerializer

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):

        internship_serializer = InternshipSerializer(
            Internship.objects.all(),
            context={'request': request},
            many=True
        )

        project_serializer = ProjectSerializer(
            Project.objects.all(),
            context={'request': request},
            many=True
        )

        competition_serializer = CompetitionSerializer(
            Competition.objects.all(),
            context={'request': request},
            many=True
        )

        return Response(
            {
                'internship': internship_serializer.data,
                'competition': competition_serializer.data,
                'project': project_serializer.data
            },
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):

        data = request.data

        serializer_context = {
            'user': request.user,
            'request': request
        }

        serializer = self.get_serializer_class()(
            data=data,
            context=serializer_context
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
