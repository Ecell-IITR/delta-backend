from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from users.models import Person
from users.serializers.auth.login import LoginSerializer


class LoginAPIView(generics.GenericAPIView):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        username = data.get("username", None)
        password = data.get("password", None)

        if not username:
            return Response(
                "Username cannot be empty!", status=status.HTTP_400_BAD_REQUEST
            )
        if not password:
            return Response(
                "Password cannot be empty!", status=status.HTTP_400_BAD_REQUEST
            )

        try:
            person = Person.objects.get(username=username)
        except Person.DoesNotExist:
            return Response(
                {"error_msg: Username not found!"}, status=status.HTTP_404_NOT_FOUND
            )

        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            update_last_login(None, user)

            return Response(
                {"token": token.key, "role": user.role_type}, status=status.HTTP_200_OK
            )

        return Response(
            {"error_msg": "Password does not match"}, status=status.HTTP_403_FORBIDDEN
        )
