from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from post.permissions import IsStudent

from post.models import (
    Competition,
    Internship,
    Project
)

from users.models import (
    Student
)


class BookmarkView(generics.GenericAPIView):

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

    def post(self, request, slug=None):
        student = Student.objects.get(person=request.user)
        keyword = request.data.get('keyword')
        slug = self.kwargs['slug']

        post = self.check_post_object(slug)

        if post is None:
            return Response({"msg": 'Slug doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)

        if keyword not in ['star', 'unstar']:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if keyword == 'star':
            post.bookmarks.add(student)

        elif keyword == 'unstar':
            post.bookmarks.remove(student)

        post.save()

        return Response({'msg': "Success"}, status=status.HTTP_201_CREATED)
