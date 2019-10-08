from django.urls import path, include

from post.views import PostViewSet

Post = PostViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

IndividualPost = PostViewSet.as_view({
    'get': 'retrieve',
    'put': 'update'
})

urlpatterns = [
    path('', Post),
    path(r'<slug:slug>/', IndividualPost)
]
