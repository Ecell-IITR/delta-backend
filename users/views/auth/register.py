from rest_framework.permissions import AllowAny
from rest_framework import viewsets

from users.serializers import (
    RegisterSerializer
)


class RegisterViewSet(viewsets.ModelViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny, ]
