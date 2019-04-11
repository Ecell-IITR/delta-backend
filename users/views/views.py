from rest_framework import generics, mixins, permissions
from rest_framework import permissions
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.response import Response 
from django.contrib.auth import authenticate, get_user_model
from rest_framework_jwt.settings import api_settings


from users.serializers.serializers import UserRegisterSerializer, UserEditSerializer
from users.utils import jwt_response_payload_handler
from users.permissions import AnonPermissionOnly, UserIsOwnerOrReadOnly

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
JWT_RESPONSE_PAYLOAD_HANDLER = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()

class AuthAPIView(APIView):
    permission_classes = [AnonPermissionOnly]
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'detail':'You are alreday authenticated'}, status=400)
        data = request.data
        username = data.get('username')
        password = data.get('password')
        qs = User.objects.filter(
            Q(username__iexact=username)|
            Q(email__iexact=username)
        )
        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj
                payload = JWT_PAYLOAD_HANDLER(user)
                token = JWT_ENCODE_HANDLER(payload)
                response = JWT_RESPONSE_PAYLOAD_HANDLER(token, user, request=request)

                return Response(response)
        return Response({
            'detail':'invalid credentials'
        },status=401)

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AnonPermissionOnly,]

    def get_serializer_context(self, *args, **kwargs):
        return {'request':self.request}

class EditAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserEditSerializer
    lookup_field = 'username'
    permission_classes = (
        permissions.IsAuthenticated,
        UserIsOwnerOrReadOnly,
    )
