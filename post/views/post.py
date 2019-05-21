from rest_framework.views import APIView
from rest_framework.response import Response
from post.serializers.post import Postserializer
from post.models.post import Post
from users.models.user import User
from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
)


class PostViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):

    lookup_field = 'slug'
    queryset = Post.objects.select_related('author', 'author__user')
    permission_classes = (IsAuthenticated,)
    serializer_class = Postserializer

    def create(self, request):
        serializer_context = {
            'author': request.user.profile,
            'request': request
        }

        serializer_data = request.data

        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer_context = {'request': request}
        serializer_instance = Post.objects.filter(author=request.user.profile)

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context,
            many=True
        )
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, slug):
        print("djabsdjka",slug)
        serializer_context = {'request': request}

        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Post.DoesNotExist:
            raise NotFound('An post with this slug does not exist.')

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, slug):
        serializer_context = {'request': request}

        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Post.DoesNotExist:
            raise NotFound('An post with this slug does not exist.')

        serializer_data = request.data

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context,
            data=serializer_data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
