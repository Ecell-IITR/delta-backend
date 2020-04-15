from django.urls import path, include
from users.views import (
    LoginAPIView,
    RegisterAPIView,
    BasicUser,
    SelfProfile
)

# User = WhoAmIViewSet.as_view({
#     'get': 'list',
#     'put': 'update'
# })

urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name="register"),
    path('auth/login/', LoginAPIView.as_view(), name="login"),
    path('user/', BasicUser.as_view(), name='basic_user'),
    path('profile/', SelfProfile.as_view(), name='self_profile')
    # path('update/<username>/', EditAPIView.as_view()),
]
