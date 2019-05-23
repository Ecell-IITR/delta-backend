from rest_framework.views import APIView
from rest_framework.response import Response
from post.serializers.bookmark import Bookmarkserializer
from post.models.post import Post
from users.models.user import User
from post.models.bookmark import Bookmark
from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
)


class BookmarkViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    queryset = Bookmark.objects.select_related('author', 'author__user')
    permission_classes = (IsAuthenticated,)
    serializer_class = Bookmarkserializer

    def create(self, request):
        post_obj = Post.objects.get(id=request.data['post_id'])
        serializer_context = {
            'author': request.user.profile,
            'request': request,
            'post': post_obj
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
        serializer_instance = Bookmark.objects.filter(
            author=request.user.profile)

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context,
            many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class BookmarkDestroyAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Bookmark.objects.all()

    def destroy(self, request):
        post_obj = Post.objects.get(id=request.data['post_id'])
        try:
            bookmark = Bookmark.objects.get(
                author=request.user.profile, post=post_obj)
        except Bookmark.DoesNotExist:
            raise NotFound('A comment with this ID does not exist.')

        bookmark.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
