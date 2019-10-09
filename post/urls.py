from django.urls import path, include

from post.views import (
    PostViewSet,
    BookmarkView
)

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
    path(r'<slug:slug>/', IndividualPost),
    path(r'bookmark/<slug:slug>/', BookmarkView.as_view())
]
