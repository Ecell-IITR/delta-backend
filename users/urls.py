from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from users.views import (
    LoginAPIView,
    RegisterAPIView,
    WhoAmIViewSet
)
from users.views import (FollowUserView, FollowersView,
                         FollowingView, DeleteFollow)

User = WhoAmIViewSet.as_view({
    'get': 'list',
    'put': 'update'
})


urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name="register"),
    path('auth/login/', LoginAPIView.as_view(), name="login"),
    path('auth/jwt/', obtain_jwt_token),
    path('auth/jwt/refresh/', refresh_jwt_token),
    path('user/', User),
    # path('update/<username>/', EditAPIView.as_view()),
    path('follows/', FollowUserView.as_view(), name="follow"),
    path('follows/<int:id1>/<int:id2>',
         DeleteFollow.as_view(), name="delete_follow"),
    path('followers/<int:pk>', FollowersView.as_view(), name="followers"),
    path('following/<int:pk>', FollowingView.as_view(), name="followers")

]
