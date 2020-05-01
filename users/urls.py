from django.urls import path, include, re_path
from users.views import (
    LoginAPIView,
    RegisterAPIView,
    BasicUser,
    SelfProfile,
    OrganizationList
)
from users.views import ActionView, FollowersList, FollowingList

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
    re_path(r'action/(?P<action_key>[0-9]+)/(?P<username>[0-9a-zA-Z]+)/', ActionView.as_view(), name="follow-user"),
    path('followers-list/', FollowersList.as_view(), name="followers-list"),
    path('following-list/', FollowingList.as_view(), name="following-list")

]
