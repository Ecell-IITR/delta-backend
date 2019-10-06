from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics

from users.serializers import (
    LoginSerializer
)


class LoginAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = LoginSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user, context=request)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
