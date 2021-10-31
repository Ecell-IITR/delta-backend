from rest_framework.permissions import AllowAny
from rest_framework import generics

from users.serializers import RegisterSerializer


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [
        AllowAny,
    ]
