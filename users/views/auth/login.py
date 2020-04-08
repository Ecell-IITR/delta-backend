from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login


class LoginAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)

        if not username:
            return Response('Username cannot be empty!', status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response('Password cannot be empty!', status=status.HTTP_400_BAD_REQUEST)
        try:
            user = authenticate(username=username, password=password)
        except:
            raise AuthenticationFailed

        token, created = Token.objects.get_or_create(user=user)
        update_last_login(None, user)

        return Response({'token': token.key, 'role': user.role_type}, status=status.HTTP_200_OK)
