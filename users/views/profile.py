from rest_framework import generics, status, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models.profile import Profile
from users.models.user import User
from users.serializers.profile import ProfileViewSerializer, ProfileUpdateSerializer
from users.permissions import UserIsOwnerOrReadOnly
from rest_framework.generics import RetrieveAPIView


# class ProfileView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
#     serializer_class = ProfileViewSerializer
#     queryset = Profile.objects.select_related('user')
#     lookup_field = 'username'

#     def get(self, request, username=None):
#         try:
#             profile = self.queryset.get(user__username=username)
#         except Profile.DoesNotExist:
#             raise NotFound('A profile with this username does not exist.')
#         return self.retrieve(request, )


#     def post(self, request):
#         return self.create(request)

#     def update(self, request, username=None):
#         return self.update(request, username)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except:
            return Response({"error": "Given User object not found."}, status=404)

    def post(self, request, username):
        data = request.data
        user = self.get_object(username)
        data['user'] = user.id
        serializer = ProfileViewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class UpdateProfile(APIView):
    permission_classes = [IsAuthenticated, ]

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except:
            return Response({"error": "Given User object not found."}, status=404)

    def put(self, request, username, format=None):
        instance = self.get_object(username)
        data = request.data
        serializer = ProfileUpdateSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class ProfileRetrieveAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.select_related('user')
    serializer_class = ProfileViewSerializer

    def retrieve(self, request, username, *args, **kwargs):
        try:
            profile = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            return Response({"error": "Given User object not found."}, status=404)

        serializer = self.serializer_class(profile, context={
            'request': request
        })

        return Response(serializer.data, status=status.HTTP_200_OK)
