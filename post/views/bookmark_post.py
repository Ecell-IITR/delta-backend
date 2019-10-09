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

    def post(self, request, slug=None):
        """
        This view marks posts as starred or unstarred
        We recieve the following data:
        slug: slug
        keyword: str  (star, unstar)
        """

        data = request.data

        student = Student.objects.get(person=request.user)

        keyword = data['keyword']

        slug = self.kwargs['slug']

        if Internship.objects.get(slug=slug):
            post = Internship.objects.get(
                slug=slug
            )

        elif Project.objects.get(slug=slug):
            post = Project.objects.get(
                slug=slug
            )

        elif Competition.objects.get(slug=slug):
            post = Competition.objects.get(
                slug=slug
            )

        else:
            return Response(
                {
                    "error_message": 'Slug doesn\'t exists'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if keyword not in ['star', 'unstar']:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )

        if keyword == 'star':
            post.bookmarks.add(student)

        elif keyword == 'unstar':
            post.bookmarks.remove(student)

        post.save()

        return Response(
            {
                'success': "Successfully starred!"
            },
            status=status.HTTP_200_OK
        )
