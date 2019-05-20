from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from users.views.user import LoginAPIView, RegisterAPIView, EditAPIView
from users.views.profile import ProfileView, UpdateProfile, ProfileRetrieveAPIView

urlpatterns = [
    path('auth/login', LoginAPIView.as_view(), name="login"),
    path('auth/register', RegisterAPIView.as_view()),
    path('auth/jwt', obtain_jwt_token),
    path('auth/jwt/refresh', refresh_jwt_token),
    path('update/<username>/', EditAPIView.as_view()),
    path('create/profile/<username>/',ProfileView.as_view()),
    path('get/profile/<username>/',ProfileRetrieveAPIView.as_view()),
    path('update/profile/<username>/',UpdateProfile.as_view()),
]
