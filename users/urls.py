from django.urls import path, include
from users.views import (
    LoginAPIView,
    RegisterAPIView,
    WhoAmIViewSet
)

User = WhoAmIViewSet.as_view({
    'get': 'list',
    'put': 'update'
})

urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name="register"),
    path('auth/login/', LoginAPIView.as_view(), name="login"),
    path('user/', User),
    # path('update/<username>/', EditAPIView.as_view()),
]
