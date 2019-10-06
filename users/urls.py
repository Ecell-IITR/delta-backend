from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from users.views import (
    LoginViewSet,
    RegisterViewSet
)
router = SimpleRouter()
router.register(
    r'auth/register',
    RegisterViewSet,
    base_name='Register'
)
router.register(
    r'auth/login',
    LoginViewSet,
    base_name='Login'
)

urlpatterns = [
    # path('auth/login', LoginAPIView.as_view(), name="login"),
    path('auth/jwt', obtain_jwt_token),
    path('auth/jwt/refresh', refresh_jwt_token),
    # path('get/user', UserInfo.as_view()),
    # path('update/<username>/', EditAPIView.as_view()),
]

urlpatterns += router.urls
