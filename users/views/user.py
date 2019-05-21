from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from users.models.user import User
from users.serializers.user import RegisterSerializer, EditSerializer, LoginSerializer
from users.permissions import UserIsOwnerOrReadOnly


class LoginAPIView(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny, ]

    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}


class EditAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = EditSerializer
    lookup_field = 'username'
    permission_classes = [
        IsAuthenticated,
        UserIsOwnerOrReadOnly,
    ]
