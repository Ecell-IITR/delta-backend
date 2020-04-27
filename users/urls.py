from django.urls import path, include
from users.views import (
    LoginAPIView,
    RegisterAPIView,
    BasicUser,
    SelfProfile,
    OrganizationList
)
from users.views import (FollowUserView, FollowersView,
                         FollowingView, DeleteFollow)

# User = WhoAmIViewSet.as_view({
#     'get': 'list',
#     'put': 'update'
# })


urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name="register"),
    path('auth/login/', LoginAPIView.as_view(), name="login"),
    path('user/', BasicUser.as_view(), name='basic-user'),
    path('profile/', SelfProfile.as_view(), name='self-profile'),
    path('organization-list/', OrganizationList.as_view(), name='organization-list'),
    # path('update/<username>/', EditAPIView.as_view()),
    path('follows/', FollowUserView.as_view(), name="follow"),
    path('follows/<int:id1>/<int:id2>',
         DeleteFollow.as_view(), name="delete_follow"),
    path('followers/<int:pk>', FollowersView.as_view(), name="followers"),
    path('following/<int:pk>', FollowingView.as_view(), name="followers")

]
